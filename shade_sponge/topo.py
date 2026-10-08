"""Topography: surface-water routing on the DTM, buildings as obstacles.
Priority-Flood + FIFO (Barnes et al. 2014 (to add)): depressions are filled implicitly and every cell gets one receiver
(the 8-neighbour that flooded it), so water also drains through pits and flat streets towards the grid edge.
ASSUMPTION: no sewer inlets and no inflow from outside the grid. The result shows where surface water would converge,
not where it ends up."""
import heapq, collections, numpy as np

N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def route(z):
    """z: 2-D elevation without NaN -> receiver per cell (flat index, -1 = outlet) and processing order (downstream first)."""
    H, W = z.shape
    zf = z.ravel().tolist()
    n = H * W
    recv, seen, order = [-1] * n, bytearray(n), []
    pq, pit = [], collections.deque()
    for r in range(H):
        for c in (range(W) if r in (0, H - 1) else (0, W - 1)):
            i = r * W + c
            seen[i] = 1
            heapq.heappush(pq, (zf[i], i))
    while pq or pit:
        zc, c = pit.popleft() if pit else heapq.heappop(pq)
        order.append(c)
        r, k = divmod(c, W)
        for dr, dk in N8:
            rr, kk = r + dr, k + dk
            if 0 <= rr < H and 0 <= kk < W:
                j = rr * W + kk
                if not seen[j]:
                    seen[j] = 1
                    recv[j] = c
                    if zf[j] <= zc:
                        pit.append((zc, j))          # inside a depression or flat: filled to the spill level
                    else:
                        heapq.heappush(pq, (zf[j], j))
    return np.array(recv), np.array(order)


def accumulate(recv, order, w):
    """Upstream sum of w (e.g. contributing open area in m²) at every cell."""
    a, rv = w.ravel().astype(float).tolist(), recv.tolist()
    for c in reversed(order.tolist()):
        if rv[c] >= 0:
            a[rv[c]] += a[c]
    return np.array(a).reshape(w.shape)


def flow_distance(recv, order, mask, res=1.0):
    """Distance (m) along the flow path from each cell to the first cell in mask (inf if the path never reaches it)."""
    W = mask.shape[1]
    m, rv = mask.ravel().tolist(), recv.tolist()
    d = [0.0 if v else np.inf for v in m]
    for c in order.tolist():
        j = rv[c]
        if not m[c] and j >= 0 and d[j] < np.inf:
            d[c] = d[j] + res * (1.0 if (c - j) in (1, -1, W, -W) else 1.4142)
    return np.array(d).reshape(mask.shape)
