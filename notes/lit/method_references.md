# Method references: verification (10 Oct 2026, issue #5)

Verified = bibliographic data matched in an independent record (Crossref API, or the document itself opened). Nothing below was read beyond the front matter unless stated.

| Reference | Citation | DOI / URL | How verified | Status |
|---|---|---|---|---|
| NEH-630 ch. 10 | USDA-NRCS, National Engineering Handbook Part 630 Hydrology, Chapter 10 "Estimation of Direct Runoff from Storm Rainfall", 210-VI-NEH, July 2004 | No DOI. https://directives.nrcs.usda.gov/ (Part 630 index); copy: https://prod.damtoolbox.org/images/3/35/NEH10.pdf | PDF downloaded; title page reads "Part 630 Hydrology, National Engineering Handbook, Chapter 10, Estimation of Direct Runoff from Storm Rainfall". The July 2004 date comes from a search summary, not from the page text I opened | Verified (title); date 🟡. NRCS has an update agreement for ch. 10 (2015), revised issue not checked |
| TR-55 | USDA-NRCS (SCS), Urban Hydrology for Small Watersheds, Technical Release 55, 2nd ed., June 1986 | No DOI. https://ponce.sdsu.edu/tr55.pdf (copy); https://www.govinfo.gov/content/pkg/CZIC-gb980-u73-1986/html/CZIC-gb980-u73-1986.htm | PDF downloaded; title page reads "Urban Hydrology for Small Watersheds TR-55, Technical Release 55, June 1986" | Verified |
| Gash 1979 | Gash, J.H.C. (1979). An analytical model of rainfall interception by forests. Q. J. R. Meteorol. Soc. 105:43-55 | 10.1002/qj.49710544304 | Crossref record matches title, journal, volume, pages, year; paper itself not opened (paywalled) | Bibliography verified; formulas not checked against primary text 🟡 |
| Gash et al. 1995 | Gash, J.H.C., Lloyd, C.R., Lachaud, G. (1995). Estimating sparse forest rainfall interception with an analytical model. J. Hydrol. 170:79-86 | 10.1016/0022-1694(95)02697-N | Crossref record matches (volume 170, pages 79-86, Aug 1995); not opened | Bibliography verified 🟡 content |
| Deb et al. 2002 | Deb, K., Pratap, A., Agarwal, S., Meyarivan, T. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. IEEE Trans. Evol. Comput. 6(2):182-197 | 10.1109/4235.996017 | Crossref record matches title, volume 6, pages 182-197, April 2002 | Verified |
| Parameter source for Gash tables | Zhang et al. (2006). Modelling and measurement of two-layer-canopy interception losses in a subtropical evergreen forest of central-south China. Hydrol. Earth Syst. Sci. 10:65-77 | 10.5194/hess-10-65-2006 | Open-access PDF opened; its Table 2 sets the original and sparse (Gash et al. 1995; Valente et al. 1997) forms side by side | Read (tables only) |
| i-Tree interception | i-Tree Eco Precipitation Interception Model Descriptions; i-Tree Streets/Design/Eco Rainfall Interception Model Comparisons | https://www.itreetools.org/documents/61/iTree_Eco_Precipitation_Interception_Model_Descriptions.pdf ; https://www.itreetools.org/documents/63/iTree_Streets_Design_Eco_Rainfall_Interception_Model_Comparisons.pdf | Both PDFs opened; S_L = 0.0002 m, S_vmax = S_L LAI, c = 1 - exp(-k LAI), k = 0.7 trees | Read |
| Wang et al. 2008 | Wang, J., Endreny, T.A., Nowak, D.J. (2008). Mechanistic simulation of tree effects in an urban water balance model. JAWRA 44:75-85 | 10.1111/j.1752-1688.2007.00139.x | Crossref record only; its parameters read through the i-Tree documents | Bibliography verified |

## Sealed surface "45% to 72% (1956-2009)"

- Claim in topic_decision section 7 and slides/outline_20oct.md slide 2 (bullet and script): "Barcelona's sealed surface grew from 45% to 72% of the municipality between 1956 and 2009".
- Found in the City of Barcelona's Atles de Resiliencia (flood section, English page https://coneixement-eu.bcn.cat/widget/atles-resiliencia/en_index_inundabilitat.html), fetched 10 Oct 2026. It states impermeable surface grew by more than 2,800 hectares, from 45% to 72% of the municipal area, and credits the chart to Barcelona Regional's "Impact Study on Climate Change in Barcelona". The Spanish/Catalan source is the chapter https://lameva.barcelona.cat/barcelona-pel-clima/sites/default/files/cap03_inudabilitat_urbana-20180227.pdf (found by search, not opened).
- Status: the figure is real but secondary; the primary study (Barcelona Regional impact study) is not located or opened. Recommended citation: "Ajuntament de Barcelona, Atles de Resiliencia (citing Barcelona Regional, Estudi d'impacte del canvi climatic a Barcelona)". Keep it only with that citation, or drop it; do not cite as a peer-reviewed number.
- The same page gives the "3 episodes per year above 60 mm/h in the first 20 minutes" sentence without a named source (chart credited to BCASA, 1995-2018). The Urban Resilience Hub page repeats the 45%-72% figures but mislabels them "pervious".
- Caveat: "sealed" here means the atlas's "impermeable surface"; the Porta grid (roofs 29% plus sealed open space 52%, methodology 4b) is a different quantity and date (2021).

## Not found
- Primary Barcelona Regional impact study: not found as a standalone document.
- Gash 1979 and Gash et al. 1995 full text: paywalled, not in `papers/`; formulas below in the definition note are taken from Zhang et al. 2006 Table 2 and flagged 🟡.
