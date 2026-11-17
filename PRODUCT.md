# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

People looking to buy a residential plot in or around Chennai: first-time buyers, families buying land to build on later, NRIs buying remotely, and investors comparing growth corridors.

Their job: find plot layouts in the corridor they want, see the approval status up front, shortlist a few, and reach the developer to arrange a site visit.

A second audience is plot developers who want their layouts listed.

## Product Purpose

**Chennai Plots** is a plots-only property marketplace for Chennai. It lists residential plot layouts from developers so buyers can compare them by corridor, locality and approval, shortlist them and enquire. It is a new identity (November 2026); it replaces the earlier i5 Housing & Properties company site that lived in this repository.

Success means a buyer finds a relevant layout and sends an enquiry, or a developer asks to list a layout.

## Positioning

Plots only: no flats, villas or farmland. Approval status is shown on every listing, and buyers deal with the developer directly. Chennai Plots is a listing marketplace, not a seller.

## Operating Context

- Buyers browse by corridor (GST Road, OMR, West Chennai, Oragadam) and locality, then filter by approval and by verified developers.
- Prices are not published. Every listing shows "Price on request".
- Shortlists are stored in the visitor's browser (localStorage); there are no accounts.
- Enquiries are designed to open a pre-filled WhatsApp message. **The contact number is a placeholder (+91 00000 00000)**, so enquiry forms currently show a notice and send nothing. Set `PHONE` and `WHATSAPP` in `scripts/build_site.py` and rebuild to switch them on.
- Buyers check DTCP or CMDA approval, RERA registration, and title documents (sale deed, approval copy and layout plan, encumbrance certificate, patta, parent documents).

## Capabilities and Constraints

- The site is generated: `python3 scripts/build_site.py` writes `index.html` and one page per real listing into `projects/`. Edit the script, not the generated files.
- Static HTML with inline CSS and JS. The Archivo font and the hero video are served from this repo through the jsDelivr CDN, pinned to a commit hash.
- Real listings (bookable, each with a detail page): four plot layouts from i5 Housing & Properties, shown as one verified developer: i5 Palace (Nellikuppam - Keezhur, Chengalpattu, 92 acres, DTCP, gated, GST Road corridor), i5 Aurowin Enclave, i5 Wonder City, i5 Palace City (DTCP residential plots, Chennai, exact area on request).
- Terminology: "plot layout", "corridor", "locality", "DTCP", "CMDA", "RERA", "patta", "encumbrance certificate", "verified developer", "sample listing".
- "Verified developer" means the developer has confirmed its listing details with Chennai Plots. Only i5 Housing & Properties holds it today.
- Undecided: the real contact number, who operates Chennai Plots as a business, whether listing is free for developers, and whether a Tamil version is needed.

## Brand Commitments

- Name: Chennai Plots. Tagline under the logo: "Plots-only marketplace".
- Logo: a green plot-grid mark with a clay corner peg, drawn inline as SVG, plus the wordmark with "Plots" in green.
- Voice: plain, factual, buyer-first. Short sentences. Tell buyers to verify documents themselves.
- The earlier i5 identity (i5 logo, orange palette, "Think high, achieve high") is retired from the site. The logo files remain in `assets/` but are unused.

## Evidence on Hand

Confirmed and usable as fact:

- The four i5 plot layouts and their details listed above. i5 Housing & Properties has been in business since 2010.
- General facts about DTCP, CMDA and TNRERA used in the buying guide.

Assets:

- Real: the Tamil Nadu aerial hero video and posters (`assets/hero/`).
- Stock: all listing photos are Unsplash images and carry an "Illustrative image" tag. Do not present them as real sites.

Placeholder content, by the user's request:

- Six **sample listings** from fictional developers (Lorem Builders, Ipsum Developers, Dolor Constructions, Amet Estates). Each is badged "Sample listing", cannot be booked, has no detail page and shows no price, size or approval. Replace them with real listings, or remove them, before promoting the site.
- Developer avatars are initials badges, not photos or logos.
- The contact number.

Absent, and must not be invented: prices, plot sizes, availability, approval or RERA registration numbers, testimonials, reviews, listing counts beyond what is on the page, and claims about how many buyers or developers use the site.

## Product Principles

1. **Plots only.** Never add other property types; the narrow focus is the point.
2. **Approval up front.** Every listing states its declared approval, or says it is not declared.
3. **Marked honestly.** Sample, illustrative and placeholder content is always labelled as such.
4. **Buyer verifies, developer sells.** The site helps buyers compare and reach developers; it never implies that it has checked title documents or that it sells plots.
