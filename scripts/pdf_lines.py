"""Vector lines out of a PDF plan, without a PDF library: python scripts/pdf_lines.py <file.pdf> [out.json]
For the eWise utility plans (scripts/utilities_pdf.py): reads each page's content stream (Flate) and returns every stroked
polyline with its stroke colour and width, in PDF points after the current transformation matrix. Handles the operators the
eWise plans use (q Q cm, RG/SCN/G/K stroke colours, w, m l c re h, S s f F B b n, Form XObjects through Do); text, images,
clipping and dashes are ignored. Raw plans stay on the OMEN: run it only on gitignored files and never commit its output."""
import json, re, sys, zlib

NUM = re.compile(rb"[-+]?(?:\d+\.\d*|\.\d+|\d+)")
TOK = re.compile(rb"/[^\s/\[\]()<>{}%]+|\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]*>|\[|\]|[^\s/\[\]()<>{}%]+")


def objects(b):
    out = {}
    for m in re.finditer(rb"(\d+) 0 obj(.*?)endobj", b, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def stream(v):
    if b"stream" not in v:
        return None
    s = v.split(b"stream", 1)[1].lstrip(b"\r\n")
    s = s[: s.rfind(b"endstream")]
    try:
        return zlib.decompress(s) if b"/FlateDecode" in v.split(b"stream", 1)[0] else s
    except zlib.error:
        return zlib.decompressobj().decompress(s)


def mul(a, b):  # PDF matrices [a b c d e f]: a then b
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3], a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def run(data, O, res, ctm, out):
    """Interpret one content stream; res = the resource dict bytes (for Do); appends dict(c, w, pts) to out."""
    st, stack = dict(ctm=ctm, c=(0, 0, 0), w=1.0), []
    path, cur, ops = [], [], []
    xo = dict(re.findall(rb"/(\w+)\s+(\d+) 0 R", res.split(b"/XObject", 1)[1].split(b">>", 1)[0])) if b"/XObject" in res else {}
    P = lambda x, y: (x * st["ctm"][0] + y * st["ctm"][2] + st["ctm"][4], x * st["ctm"][1] + y * st["ctm"][3] + st["ctm"][5])
    for t in TOK.findall(data):
        if NUM.fullmatch(t):
            ops.append(float(t)); continue
        if t[:1] in b"/([<]" :
            ops.append(t); continue
        o = t
        n = [x for x in ops if isinstance(x, float)]
        if o == b"q": stack.append(dict(st))
        elif o == b"Q": st = stack.pop() if stack else st
        elif o == b"cm" and len(n) >= 6: st["ctm"] = mul(n[-6:], st["ctm"])
        elif o in (b"RG", b"SCN", b"SC") and len(n) >= 3: st["c"] = tuple(round(v, 3) for v in n[-3:])
        elif o == b"G" and n: st["c"] = (n[-1],) * 3
        elif o == b"K" and len(n) >= 4: st["c"] = tuple(round((1 - v) * (1 - n[-1]), 3) for v in n[-4:-1])
        elif o == b"w" and n: st["w"] = n[-1] * abs(st["ctm"][0])
        elif o == b"m" and len(n) >= 2:
            if len(cur) > 1: path.append(cur)
            cur = [P(*n[-2:])]
        elif o == b"l" and len(n) >= 2: cur.append(P(*n[-2:]))
        elif o == b"c" and len(n) >= 6: cur.append(P(*n[-2:]))          # curve: keep its end point (plans are polylines)
        elif o == b"re" and len(n) >= 4:
            x, y, w, h = n[-4:]
            if len(cur) > 1: path.append(cur)
            path.append([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h), P(x, y)]); cur = []
        elif o == b"h" and len(cur) > 1: cur.append(cur[0])
        elif o in (b"S", b"s", b"B", b"b", b"B*", b"b*", b"f", b"F", b"f*", b"n"):
            if len(cur) > 1: path.append(cur)
            if o not in (b"f", b"F", b"f*", b"n"):  # stroked paths only
                out += [dict(c=st["c"], w=round(st["w"], 3), pts=[(round(x, 2), round(y, 2)) for x, y in p]) for p in path]
            path, cur = [], []
        elif o == b"Do" and ops and isinstance(ops[-1], bytes):
            k = xo.get(ops[-1][1:])
            v = O.get(int(k)) if k else None
            if v is not None and b"/Form" in v.split(b"stream", 1)[0]:
                head = v.split(b"stream", 1)[0]
                mm = re.search(rb"/Matrix\s*\[([^\]]*)\]", head)
                M = [float(x) for x in mm.group(1).split()] if mm else [1, 0, 0, 1, 0, 0]
                run(stream(v), O, head, mul(M, st["ctm"]), out)
        ops = []
    return out


def pages(fn):
    b = open(fn, "rb").read()
    O = objects(b)
    kids = re.search(rb"/Type\s*/Pages.*?/Kids\s*\[([^\]]*)\]", b, re.S)
    order = [int(x) for x in re.findall(rb"(\d+) 0 R", kids.group(1))] if kids else sorted(k for k, v in O.items() if re.search(rb"/Type\s*/Page[^s]", v))
    res = []
    for k in order:
        v = O[k]
        box = [float(x) for x in re.search(rb"/MediaBox\s*\[([^\]]*)\]", v).group(1).split()]
        cs = re.search(rb"/Contents\s*(?:\[([^\]]*)\]|(\d+) 0 R)", v)
        ids = [int(x) for x in re.findall(rb"(\d+) 0 R", cs.group(1))] if cs and cs.group(1) else ([int(cs.group(2))] if cs else [])
        r = re.search(rb"/Resources\s*(\d+) 0 R", v)
        rd = O[int(r.group(1))] if r else v
        lines = []
        for i in ids:
            run(stream(O[i]) or b"", O, rd, [1, 0, 0, 1, 0, 0], lines)
        res.append(dict(page=len(res) + 1, box=box, lines=lines))
    return res


if __name__ == "__main__":
    P = pages(sys.argv[1])
    for p in P:
        from collections import Counter
        c = Counter((l["c"], l["w"]) for l in p["lines"])
        print(f"page {p['page']} box {p['box']}: {len(p['lines'])} polylines; colour,width: {c.most_common(12)}")
    if len(sys.argv) > 2:
        json.dump(P, open(sys.argv[2], "w"))
