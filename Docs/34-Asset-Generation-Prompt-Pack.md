# 34 — Asset Generation Prompt Pack

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-34 |
| Version | 1.2 |
| Status | **PROPOSED — not approved.** This is a run sheet, not a production order. Nothing in it authorises spending generation credits. |
| Owner | Product Design Lead (prompt approval) + Frontend Lead (intake) |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `30` §3/§4/§5/§11, `31`, `32`, `33`, `21` §7, `26` §4.1, `36` §3 (nothing generated here may be served from an origin the CSP gate rejects), `37` §7.1 (where a generated file is consumed) |
| Blocks | nothing; it is consumed by whoever runs the artwork, after `OD-DOC-34` and `OD-DOC-30` close |

---

## 1. Why this document exists, and where the artwork now stands

The owner directed placeholder-first delivery: SVG or a blank container at design time, real imagery
when the upload and storage system exists (`30` §5.3, `OD-DOC-36`). The same owner said that if this
tool cannot generate an asset, the prompt should be written for another model to run
(ChatGPT, Gemini, and similar). So the deliverable here is **prompts, not pictures** — and the split is
measured from the register rather than asserted.

From `design-assets/manifests/asset-inventory.csv`, 105 rows (93 at first issue; the 12 website-section
rows of §4.7 were registered on 2026-10-22 on the owner's direction):

| Production route | Rows | Asset types | Run through a model? |
|---|---:|---|---|
| **Generatable raster** | **36** | `illustration` 12, `empty-state` 10, `category-image` 6, `hero` 2, `og-image` 2, `success-state` 1, `error-state` 1, `pattern` 1, `feature-graphic` 1 | **Yes** — §4's prompts |
| Vector / authored | 68 | `nav-icon` 43, `category-icon` 6, `infographic` 4, `map-marker` 4, `logo` 3, `favicon` 2, `pwa-icon` 2, `mark` 1, `app-icon` 1, `store-icon` 1, `photo-placeholder` 1 | **No** — `30` §11. A model produces a 1024 px raster where a 1 KB path is required |
| Real capture only | 1 | `screenshot-set` | **No** — must come from an approved build, and `33`/`29` forbid an invented one |

Of the 36 generatable rows, **30 have a prompt that can run today and 6 are `[BLOCKED]`**: the six
`category-image` rows depend on the launch-category decision (`OD-DOC-27` 3 vs 4 vs 6 vs 2,
`OD-DOC-28` salon/beauty, `OD-DOC-33` whether the asset unit is family, service or variant). Generating
them now means generating them twice.

**The first 18 of those 30 were run and intaken on 2026-10-22; the 12 website-section rows of §4.7 are
registered and waiting to be run.** What "run" bought is recorded in `32` §6 and the register: 18 masters,
58 exports, 22 manifest records, all `GENERATED` and **none `APPROVED`** — production of an image is not
acceptance of a design (`DEC-03`). What has *not* changed is the warning this section was written to give:
`OD-DOC-30` (palette approval), `OD-DOC-34` (storage and CSP), `OD-COM-12` (IP position on generated
design assets) and `OD-DOC-33` are all still open, generation costs credits that cannot be refunded by
deleting the output, and `30` §11 shows that most of the remaining inventory is un-generatable at any price.

---

## 2. The style lock — paste this ahead of every prompt

> **What actually got past the model on 2026-10-22 is a reworded form of this block, and the wording
> below is kept as the requirement record.** The `AMM-BRAND-PATTERN-BACKGROUND` run was **refused by
> ChatGPT's content filter** ("the image we created may violate our content policies") — nothing about the
> subject was sensitive; the trigger was the `STRICTLY FORBIDDEN` wall itself. A classifier reading eight
> lines of *identifiable people*, *visible faces*, *photorealistic skin*, *watermarks* and *brand names*
> sees a dense bag of person- and identity-words whether they arrive negated or not, and negation is weak
> signal. The operative wording is therefore the four rules in `maintenance/prompts/00-START-HERE.md`
> §"Why the wording was rewritten" — ask for the person-free image **positively**, replace the prohibition
> wall with a short `KEEP THE IMAGE TO:` line, keep only the *no text / no numbers* negations, and move
> every person-, face-, brand- or plate-named **reject criterion out of the prompt and into the human
> "check before saving" list**. No rejection was dropped, only relocated: the model never sees them, the
> reviewer still enforces all of them.

Every prompt below is the style block plus a subject line. Do not run a subject on its own; the
consistency the brief asks for comes from the block, and it is what makes 18 files look like one system.

```
STYLE LOCK — AmmPal Service illustration system
Flat modern vector-style illustration, 2 colours plus one accent, thin even outlines.
Line colour #2C4551. Fill colour #E9F3F4. Accent colour #0A6E77. Highlight #C9A227 used only
as one small element and never as text. Background #FFFFFF, perfectly even, no vignette.
Single scene, one-point perspective, camera at eye level, generous negative space, subject
occupies about 60% of the frame and sits centred with at least 8% clear margin on every side.
Warm neutral domestic and service-trade setting in India: ceiling split air-conditioner, window
air-conditioner, front-load washing machine, refrigerator, microwave, water purifier under a sink,
service toolbox, screwdriver, spirit level, mask and gloves. Clean, calm, competent, unhurried.
STRICTLY FORBIDDEN: any text, letters, numbers, logos, watermarks, UI elements, buttons,
speech bubbles, price tags, tick marks that form a checkmark inside a box, visible faces,
identifiable people, brand names on appliances, photorealistic skin, stock-photo smile staging,
lens flare, neon, purple or violet, gradient meshes, drop shadows on the illustration,
isometric 3D "tech" art, mascots, confetti, stars bursting, cluttered backgrounds.
```

Why the numbers in that block are those exact numbers: `#2C4551`, `#E9F3F4`, `#0A6E77`, `#C9A227` and
`#FFFFFF` are `30` §3.2–§3.4's measured tokens, so a generated file that is accepted can be placed
against a UI that already uses them. If `OD-DOC-30` changes the palette, this block changes in one edit
and every prompt re-runs — which is the reason it is one block and not 24 copies.

**The universal negative prompt**, for tools that take a separate negative field:

```
text, letters, words, numbers, watermark, logo, brand mark, user interface, screenshot, button,
icon set, speech bubble, caption, signature, visible face, portrait, person's identity, tattoo,
photorealism, skin texture, neon, glow, lens flare, purple, violet, magenta, pink, gradient mesh,
isometric, low poly, 3D render, drop shadow, reflection, confetti, sparkle, stars, cluttered, busy,
blurry, jpeg artifacts, extra limbs, deformed hands, distorted appliance, wrong number of knobs
```

---

## 3. Three limits that change the plan, stated before the prompts

**3.1 Most image models do not emit an alpha channel.** `32` §4 requires transparency for chips,
markers, empty-state art over a tinted card, and every icon. A generated PNG will arrive on an opaque
ground. So for any row whose `transparency` column says yes: generate on the **exact** background the
composition will sit on (white `#FFFFFF` or `#E9F3F4`), and knock the ground out in a vector pass, or
accept the flat ground and change the UI to match it. Do not ask a model for a transparent background
and believe the result — check the pixel, do not check the preview thumbnail.

**3.2 A model draws an approximation of a number, not a size.** `AMM-WEB-HERO-HOMEPAGE-1600` is 1600 ×
1000 px (`32` §3). Models output their own grid (1024, 1536, 1792 and similar). So the run sheet records
**the target size and the nearest generation aspect ratio**, and the resize/crop happens in the intake
step (`32` §4) with a measured byte ceiling. Never ship a generated file at its native size and call it
the spec.

**3.3 Generated files cannot be claimed as brand-owned until `OD-COM-12` closes.** `26` records
design-asset IP as "not yet documented". Until that row is decided with the development partner, a
generated illustration may be used as a **placeholder that looks like the intended artwork**, and may
not be presented as the brand's property, registered, or shipped in a store listing as original work.
This is the single reason the intake status in `32` §4 is `GENERATED` and never `APPROVED`.

---

## 4. Run sheet — 36 rows

`Ratio` is the generation aspect ratio to request; `Target` is the shipped size from the inventory,
produced at intake. `File` is the `32` §2 name with the mandatory `-v01` suffix; a regeneration is
`-v02`, never an overwrite.

> **Status as re-measured on 2026-10-22, from `validate_assets.py` (105 rows — 18 `GENERATED`, 6
> `BLOCKED`, 77 `PLANNED`, 4 `REGISTERED`; 22 manifest records; 0 errors).** The `Status` column in
> §4.1–§4.6 was the state at first issue and the register is the authority: **every row of §4.1–§4.5 is
> now `GENERATED`** — the 4 marketing/brand rows, 5 customer empty states plus the booking success state,
> the 4 partner empty states, the 2 Control Center states and the serviceability illustration, the store
> feature graphic, both OG images and the homepage hero — and the six §4.6 `category-image` rows are
> unchanged at `BLOCKED`, with their generated PNGs held in `maintenance/holding-blocked/` because a
> `BLOCKED` row may not enter `GENERATED` (`32` §6). Two versions matter: the homepage hero ships
> **`-v02`** (the owner's choice on sight of both; `-v01` stays on disk as the rejected attempt, not as a
> deliverable), and `AMM-CUSTOMER-EMPTY-NOTIFICATIONS-600` is a visual-fail candidate — its gold bell
> breaches `30` §3's 2 % metal budget, so it owes a `-v02` before anyone calls the set finished. §4.7 adds
> the 12 website-section rows, which are registered and **not yet generated**.

### 4.1 Marketing and brand (4 rows — run these first, they set the tone)

| File | Target | Ratio | Status |
|---|---|---|---|
| `AMM-WEB-HERO-HOMEPAGE-1600-v01.png` | 1600 × 1000 | 16:10 | `PLANNED` |
| `AMM-BRAND-PATTERN-BACKGROUND-v01.svg-derivable` | 1600 × 1600 tile | 1:1 | `PLANNED` |
| `AMM-BRAND-OG-HOMEPAGE-v01.png` | 1200 × 630 | 1.91:1 | `PLANNED` |
| `AMM-WEB-OG-PARTNER-1200-v01.png` | 1200 × 630 | 1.91:1 | `PLANNED` |

**Hero.** Style lock, then:
> A wide, calm scene of a technician's open service toolbox in the foreground on a clean floor mat,
> a split air-conditioner indoor unit mounted high on a pale wall behind it, a folded ladder and a
> screwdriver resting nearby, soft daylight from the left, no people at all, the upper right third of
> the frame left as empty pale space for a headline to be placed over in the interface.

Reject if: a person appears, the scene is a workshop with tools on a pegboard (it is a **home**, and
`12` §3's booking flow is domestic), the empty space is filled with decoration, or any surface shows a
brand name.

**Pattern tile.** Style lock, but replace the colour sentence with "`#F4F8F9` ground, motifs only in
`#E9F3F4`" and add: "seamlessly repeating 2×2 grid of tiny abstract service motifs — a wrench head, a
water droplet, a fan blade, a sparkle-for-clean — drawn as flat filled shapes at 6 % opacity, evenly
spaced, no outlines". Reject if: motifs are recognisable as an icon set (they compete with real icons in
a UI), or the tile does not repeat (check by placing it 2 × 2 before intake). **This row should end as
SVG**, and the generated raster is only a reference for the traced version.

**OG images.** Style lock, then: "a 1.91:1 composition with the entire left 45 % reserved as flat empty
space for type added later in the interface, the right side carrying one appliance motif at medium
scale". The `en`/`or`/`hi` headline is **never** baked in (`30` §11: no text in images; `12` §8 i18n-03
expansion). Reject if: any letterforms appear, or the empty space is not actually empty.

`AMM-WEB-OG-PARTNER-1200` is the partner-side preview: same block, subject "a service vehicle's open
rear compartment with two neat tool cases and a rolled uniform, no logo on the vehicle, no number
plate", and **no readable number plate** — a real plate is someone's identity.

### 4.2 Customer app empty states (5 rows, 600 × 450, 4:3)

All five: style lock + "one single object centred, extremely quiet, nothing else in the frame".

| File | Subject line to append |
|---|---|
| `AMM-CUSTOMER-EMPTY-BOOKINGS-600-v01.png` | "a closed diary with a plain ribbon, lying flat on a pale surface, no text on the cover" |
| `AMM-CUSTOMER-EMPTY-NOTIFICATIONS-600-v01.png` | "a bell resting on its side on a pale surface, not ringing, no motion lines, no badge" |
| `AMM-CUSTOMER-EMPTY-SUPPORT-600-v01.png` | "a headset placed on a desk beside a closed notebook, no person, no screen" |
| `AMM-CUSTOMER-EMPTY-SLOTS-600-v01.png` | "an empty wall calendar page holder with a blank card, no printed dates, no numbers" |
| `AMM-CUSTOMER-EMPTY-TECHNICIANS-600-v01.png` | "an empty service apron hanging on a hook, neatly, no person, no name tag" |

Reject if: any numeral appears on a calendar or clock; a calendar with visible dates reads as a
statement about availability, which is exactly what an empty state must not claim (`12` §3.3's freshness
honesty). And reject any row where the object looks broken or sad — an empty state is not an error.

### 4.3 Partner app empty states (4 rows, 480 × 360, 4:3)

Same style lock. These sit in an app used one-handed and offline (`12` §4.3), so they must read at small
size: fewer elements, larger shapes, no thin detail.

| File | Subject line to append |
|---|---|
| `AMM-PARTNER-EMPTY-JOBS-480-v01.png` | "a folded job card and a pen resting on it, both plain and unprinted, side view" |
| `AMM-PARTNER-EMPTY-EARNINGS-480-v01.png` | "a closed cash envelope with a paper band, no currency symbol, no banknote portrait, no numbers" |
| `AMM-PARTNER-EMPTY-SETTLEMENT-480-v01.png` | "two plain paper receipts stacked and tied with a band, both completely blank" |
| `AMM-PARTNER-EMPTY-CALENDAR-480-v01.png` | "an empty planner stand with a blank card slid in, no week numbers, no dates" |

**The earnings and settlement rows are the sensitive ones.** Anything that resembles a banknote, a coin
stack, a rupee glyph, a payment receipt with figures, or a "you earned" badge is a financial claim made
by decoration while the real figure is absent from the server (`30` §7 prohibition 1). Blank paper only.
Reject any variant that shows a number, a currency sign or a positive amount.

### 4.4 Control Center, states and one illustration (4 rows)

| File | Target | Subject line to append |
|---|---|---|
| `AMM-CONTROL-EMPTY-TABLE-480-v01.png` | 480 × 360 | "a plain sheet of paper with completely blank horizontal rule lines and no letters, standing upright, one object only" |
| `AMM-CONTROL-DENIED-600-v01.png` | 600 × 450 | "a closed plain door with no handle on this side, or an empty flat shelf — quiet, neutral, unhurried, absolutely no warning triangle, no padlock, no red, no exclamation mark" |
| `AMM-WEB-ILLU-SERVICEABILITY-800-v01.png` | 800 × 600 | "a simple house outline on a pale map-like ground with one soft empty circle around it, no pin, no road names, no city shape that identifies a real place" |
| `AMM-CUSTOMER-SUCCESS-BOOKING-600-v01.png` | 600 × 600 | "a neatly closed diary with a plain ribbon and one small calm check-less envelope beside it, no bursting stars, no confetti, no thumbs up" |

`AMM-CONTROL-DENIED` is a correctness constraint, not a taste one: `03` §5 step 3 returns `404` so that
existence is not leaked, and `30` §3.6 repeats it as a rule. **A padlock or a red warning on that screen
tells the operator that a record exists and they cannot see it** — which the API was designed not to do.
The illustration must mean "there is nothing here", never "you are not allowed here". Reject any variant
containing a lock, a shield, a key, a triangle or the colour `#B91C1C`.

`AMM-CUSTOMER-SUCCESS-BOOKING` must be reviewed against `23` §2.3: the illustration may appear only on
the state the backend actually reported. `30` §7's prohibition 1 means a booking that is still
`REQUESTED` may not be given a "confirmed" picture by a client-side animation.

### 4.5 Store and marketing (1 row, plus one that must not be generated)

| File | Target | Note |
|---|---|---|
| `AMM-STORE-PLAY-FEATURE-1024-v01.png` | 1024 × 500 (2:1) | Style lock + "a wide quiet band: on the left the open toolbox and a split AC unit on a pale wall, on the right two-thirds empty pale space for store copy added by Google Play's own text layer". No text, no badge, no star rating, no "download now". |
| `screenshot-set` | — | **`[BLOCKED]`. Not generatable at any quality.** `32` §2 exempts it from the one-file rule because it is not one file, and `29` §4.8 accepts store screenshots **only from an actual approved build**. A mockup of an app that does not exist is the prohibited artefact, not a draft of it. |

### 4.6 Category images (6 rows — written, deliberately not runnable)

The six `AMM-SERVICE-*-CATEGORY-800` rows are `BLOCKED`. The prompts are here so that one owner decision
unblocks them, and each is style lock + a single-object subject:

| Blocked file | Subject line |
|---|---|
| `AMM-SERVICE-APPLIANCE-REPAIR-CATEGORY-800` | "a screwdriver and a small flat wrench crossed once over a plain panel, no appliance brand" |
| `AMM-SERVICE-CLEANING-CATEGORY-800` | "a spray bottle and a folded cloth on a pale surface, no bubbles shaped like characters" |
| `AMM-SERVICE-HOME-SALON-CATEGORY-800` | "a closed pair of scissors and a comb resting side by side on a pale cloth" — **plus** the BP-02 consent and HS skill note below |
| `AMM-SERVICE-BEAUTY-PARLOUR-CATEGORY-800` | "a plain cosmetics brush resting on a folded towel, no face, no skin close-up" — **plus** `BP-01`'s paramedical skill gate |
| `AMM-SERVICE-PLUMBING-CATEGORY-800` | "a pipe bend with a wrench on it and one still water droplet, no flood, no spray" |
| `AMM-SERVICE-ELECTRICAL-CATEGORY-800` | "a plain switch plate and an insulated screwdriver, no exposed wire, no spark, no lightning bolt" |

Two of these six are contested scope, not blocked work: `OD-DOC-28` records that Home salon and Beauty
parlour appear as launch categories in `06` §4.3/§4.4 **and** as Phase 4 growth in `17` §6. Their
prompts are written because the run sheet should be complete, and they carry the two rules that make
them different: `BP-02` is a **mandatory consent step** and `BP-01` is a **skill-gated paramedical
rule** (`06` §4.4) — neither of which a decorative image can satisfy, and both of which need the
compliance read that `OD-DOC-28` says has not happened. Do not generate them to "see how they look" if
the category itself has not been approved; that is scope entering through the artwork.

Also unresolved and not silently decided here: `OD-DOC-27` (the launch count is stated as 3, 4, 6 and 2
in four places) and `OD-DOC-33` (is the asset bound to a family, a service or a variant?). Six
category-image rows assume family-level binding. If the owner binds at service level, the count is
different again, and nothing here should be read as having chosen.

### 4.7 Website-section artwork (12 rows — registered 2026-10-22, not yet generated)

The owner's direction was that **the site being designed sells home appliance repair**; the other
categories are later work. These twelve rows are the appliance, booking-step and support imagery for
`12` §2.1's Home sections and for `/services`, `/pricing`, `/partner` and `/support`. They are rows of
this register (§1's generatable-raster count is 36 because of them), the full paste-ready blocks live in
`maintenance/prompts/10-website-sections.md`, and the slots they fill — with the grid box, the @2x need
and the byte ceiling for each — are measured in `39` §3.

| File | Target | Ratio | Subject | Element it serves (`12` §2.1) |
|---|---|---|---|---|
| `AMM-WEB-ILLU-AC-REPAIR-800` | 800 × 600 | 4:3 | split AC indoor unit on a pale wall | Home service categories |
| `AMM-WEB-ILLU-FRIDGE-REPAIR-800` | 800 × 600 | 4:3 | two-door refrigerator, doors closed | Home service categories |
| `AMM-WEB-ILLU-WASHING-MACHINE-REPAIR-800` | 800 × 600 | 4:3 | front-load washing machine | Home service categories |
| `AMM-WEB-ILLU-MICROWAVE-REPAIR-800` | 800 × 600 | 4:3 | countertop microwave | Home service categories |
| `AMM-WEB-ILLU-WATER-PURIFIER-REPAIR-800` | 800 × 600 | 4:3 | under-sink purifier, one visible cartridge | Home service categories |
| `AMM-WEB-ILLU-STEP-SEARCH-800` | 800 × 600 | 4:3 | house roofline under a rounded search ring | Home how-it-works, step 1 |
| `AMM-WEB-ILLU-STEP-SLOT-800` | 800 × 600 | 4:3 | blank calendar card, one space marked | Home how-it-works, step 2 |
| `AMM-WEB-ILLU-STEP-VISIT-800` | 800 × 600 | 4:3 | toolbox on a folded mat before a closed door | Home how-it-works, step 3 |
| `AMM-WEB-ILLU-TRUST-VERIFIED-800` | 800 × 600 | 4:3 | screwdriver and spanner on a folded cloth | Home trust signals |
| `AMM-WEB-ILLU-PRICING-TRANSPARENT-800` | 800 × 600 | 4:3 | estimate sheet with three blank bands | `/pricing` |
| `AMM-WEB-ILLU-SUPPORT-HELPLINE-800` | 800 × 600 | 4:3 | handset in its cradle, closed notebook | `/support`, `/toll-free` |
| `AMM-WEB-HERO-PARTNER-1600` | 1600 × 1000 | 16:10 | trade morning, left half kept empty | `/partner` hero |

Three rules distinguish this group from the eighteen already run, and they are the reason the run order
puts them after the empties:

1. **The five appliance tiles and the three step cards are a family, not twelve independent images.**
   Same camera height, same object scale, same ground; judged side by side. One tile drawn in perspective
   beside four square-on ones is the fastest way to make a catalogue page look assembled, and that is a
   `-v02` decision, not a save.
2. **Nothing in this group may carry a claim the record has not produced.** No badge, seal, star, shield
   or certificate edge in the trust drawing; no figure, currency mark or percentage in the pricing one; no
   phone number in the support one; no earnings, payout date or partner count in the partner hero. Those
   four are `34` §7's invented-artefact prohibition applied to the specific pixels a model is most likely
   to add, and the alt texts registered for these rows describe the drawing rather than restating a
   promise (`DD-06`).
3. **They ship as SVG.** Each row is `format = svg` with the `32` §4 illustration ceiling of 12 KB; a
   generated raster meets the byte figure but is not vector, so the raster is the design-time placeholder
   and the traced path is owed before any build ships with it (`30` §11). The build proceeds against
   reserved containers meanwhile (`37` §7.1) — that is the placeholder-first contract working as designed,
   not a workaround.

---

## 5. Tool notes — the block is portable, the syntax is not

The style lock and the negative prompt are plain English and work in any instruction-following image
model, including ChatGPT, Gemini and similar assistants. Three practical differences, none of which is a
capability claim about a specific vendor build — verify each against the tool in front of you:

| Concern | What to do |
|---|---|
| Aspect ratio | Ask for the ratio in words ("wide 16:10 landscape") **and** in the tool's own syntax if it has one. Whatever arrives, resize at intake to the `Target` in §4; never ship the model's native grid. |
| Size limits | Models cap well below 1600 × 1000 on some tools. If the tool cannot reach the target with headroom, generate the largest it can and mark the row `GENERATED - UPSCALE REQUIRED` in the register rather than shipping an upscaled blur. `32` §4's byte ceilings are ceilings, not targets. |
| Transparency | §3.1. Assume none. Generate on the exact ground colour and handle knockout at intake. |
| Variants | The inventory's `variants` column expects some rows in light and dark. `30` §10 proposes **light only** for launch (`OD-DOC-31` open), so generate one ground now, not two. |
| Batch naming | Name the downloaded file with the intended `File` value **at download time**, not later. Regenerations get `-v02`; a file is never overwritten (`32` §2). |

One honest limitation of this document: it was written without running any of the prompts, so no prompt
here is *proven*. They are style-locked against measured tokens and against the prohibitions in `30`,
`03`, `23`, `29` and `32`, which is a stronger basis than a guess and still weaker than a test shot.
**Run §4.1's hero first and stop.** If the hero comes back wrong, the style block is wrong, and every
later prompt would have inherited the error — 18 rows is 18 times the cost of finding out on row one.

---

## 6. Intake — what happens to a file that looks right

1. Move it into the `31` §6 folder for its surface (`02-website`, `03-customer-app`, …). The name must
   already match `32` §2's grammar; `validate_assets.py` rejects a file that lands with a name outside
   `NAME_RE`.
2. **Measure** it — actual pixel size and byte weight — and check both against the row in `32` §3/§4. A
   stated size is not a measured size.
3. Record it in `design-assets/manifests/asset-manifest.json` with: tool **and model name as the tool
   reported it**, the full prompt actually used (style block + subject, not "see `34`"), date, the
   resulting byte length and SHA-256, licence position as `UNKNOWN` until `OD-COM-12` closes, and
   `approval_status` = **`GENERATED`**.
4. Update the inventory row's `generation_status` from `PLANNED` to `GENERATED` via
   `gen_asset_inventory.py` (the CSV is generated, so edit the source and regenerate — never hand-edit
   the CSV, or the next regeneration silently reverts the work).
5. Write the `alt_text_en` from the inventory row, then read the image **as the alt text describes it**.
   If the picture does not contain what the alt says, either the alt or the picture is wrong. `32` §5
   makes `a11y_treatment` a paired column; `29` §4.8 checks both directions.
6. Show it to the owner. Only the owner's dated record turns `GENERATED` into `APPROVED`
   (`DEC-03`, and `32` §4).

**Status is never inferred.** A file that looks excellent, matches the tokens and passes the validator is
still `GENERATED`. `30`–`33`, `35`–`37` and this document are all `PROPOSED`, and a generated asset cannot make one
`APPROVED` — least of all when `26` §4.1 attaches a ₹1,00,000 instalment to the word "approval"
(`19` `R-45`, `R-47`).

---

## 7. Never generate, in any tool, at any point

- **App or web screenshots** of a product that does not exist. `29` §4.8 admits store imagery only from
  an actual approved build.
- **Reviews, ratings, install counts, "trusted by 10,000" badges, awards, press logos.**
- **Any credential-looking artefact** — a verified badge with a legal entity name, a GST or registration
  number, a certificate, a payment receipt, a UPI screen, a bank detail, an invoice with figures.
  `26` §9 `OD-COM-01`/`02`/`03` leave the commercial and tax position open, and `13` §5.2 plus
  `30` §3.5 forbid a colour or a seal implying a status the backend has not reported.
- **A real-looking partner, technician or customer.** No face, no name tag, no number plate, no
  house that could be someone's address. `09` §8's `PERSONAL` class and `06` §7's location rules both
  point the same way, and `30` §9 requires synthetic coordinates for any map imagery.
- **Anything derived from a competitor's identity** — a logo, a mascot, a distinctive uniform, a
  trade-dress colourway, or a mark whose silhouette resembles a third party's.
- **Legal, tax or compliance claims** — an icon implying certification, registration, insurance cover or
  a statutory notice. `01` FR-CMP-03 and `19` §3 treat these as unsettled; a decorative seal would
  state something the documents refuse to state (`DEC-01`: one home per decision — and this one has no
  home yet).
- **A second brand mark.** `logo`, `mark`, `app-icon`, `favicon` and `pwa-icon` are 9 of the 68
  vector rows. They come from one authored SVG master or from nothing; a model producing "a logo" 12
  times is not a design process, it is an unclaimable file (`OD-COM-12`).

---

## 8. Traceability

| This document | Referenced by / references |
|---|---|
| Palette and token values | `30` §3.2–§3.5 (measured); `OD-DOC-30` must close before §2's block is stable |
| Asset IDs, sizes, byte ceilings, naming | `32` §2/§3/§4; register `design-assets/manifests/asset-inventory.csv` |
| Which asset a screen needs | `33` §3–§4 per-screen rows, `33` §6 rollup |
| Production route, folder layout, `source-code/` deferral | `31` §5/§6 |
| Blocking decisions | `OD-DOC-27`, `OD-DOC-28`, `OD-DOC-30`, `OD-DOC-31`, `OD-DOC-33`, `OD-DOC-34`, `OD-COM-12` |
| Prohibitions drawn from backend truth | `03` §5 step 3 (`404` not `403`), `12` §3.3 freshness, `23` §2.3/§2.4, `30` §7 |
| Release gate this feeds | `29` §4.8 items 2, 4 and 8 |
| Risk if the gate is certified on placeholders | `19` `R-47`; the money trigger itself is `R-45` |
| Where a generated file is actually consumed | `37` §7.1 — the placeholder slot props every container exposes, and `CA-21`, which is the component-level statement of the same rule this document's §1 rests on: **a container that renders your file is not a screen that was approved** |
| What may load the file in a browser | `36` §3's CSP gate. Until `OD-DOC-34` closes, no origin named in a prompt's delivery instruction is admitted by `13` §5.2, so intake succeeds and production fails |

This document creates **no** `FR-*` requirement and **no** `SCR-*` screen ID. Its prompts map onto rows
of the register, and the register is where a row is created: §4.1–§4.7 name 37 rows — the 36 generatable
rows of §1 plus the `screenshot-set` that only a real build can produce — and every one of them exists in
the 105-row `design-assets/manifests/asset-inventory.csv`, citing the `doc_ref` that made it necessary. It
is a run sheet for the register, not a parallel copy of it.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.2 | 2026-10-22 | Product Design Lead + Frontend Lead (website-design pass) | Brought in line with what has actually happened since issue, with every figure re-measured rather than restated. §1's title claimed no image was made — 18 have been made and intaken, so §1 now says which and repeats that **none is approved**. Production-route split **24/68/1 → 36/68/1** and the register width **93 → 105**, because the owner said go on the 12 website-section rows (`39` §3 reserves their slots); §4 gained **§4.7** carrying them with target, ratio, subject and the `12` §2.1 element each answers to, plus the three rules that make them different from the eighteen already run — family consistency, no invented claim, SVG at intake. §4's per-row `Status` cells were still reading `PLANNED`, so §4 now opens with a measured status block: all of §4.1–§4.5 `GENERATED`, §4.6 unchanged at `BLOCKED`, the homepage hero shipping **`-v02`** by owner choice with `-v01` kept as the rejected attempt, and `AMM-CUSTOMER-EMPTY-NOTIFICATIONS-600` named as a `-v02` candidate because its gold bell breaches `30` §3's 2 % metal budget. §2 records why its `STRICTLY FORBIDDEN` wall is kept as the requirement record but is **not** the wording that gets past a content filter — the pattern run was refused, and the operative reword (positive framing, `KEEP THE IMAGE TO:`, only *no text*/*no numbers* left negative, person/face/brand/plate reject criteria relocated to the human checklist with none dropped) lives in `maintenance/prompts/00-START-HERE.md`. **No palette value, no ceiling, no `OD-*` status, no approval and no `never generate` rule changed.** | §1, §2, §4, §4.7, §8, Revision History, header |
| 1.1 | 2026-10-21 | Product Design Lead (design-engineering structure pass) | Depends On gained `36` §3 and `37` §7.1, and §8’s traceability table gained the two rows it was missing: **where a generated file is consumed** (`37` §7.1’s placeholder slot props, and `CA-21`, the component-level form of this document’s own rule — a container that renders your file is not a screen that was approved) and **what may load it in a browser** (`36` §3: until `OD-DOC-34` closes, no origin named in a delivery instruction is admitted by `13` §5.2, so intake succeeds and production fails). **No prompt was rewritten, none was run, and no image was generated** — the 24/68/1 production-route split, the style lock, the universal negative prompt, the 18 runnable rows and the 6 category-blocked rows are all as issued, and §5 still records that they were written without being executed. | §8, Depends On, Revision History, header |
| 1.0 | 2026-10-21 | Product Design Lead + Frontend Lead (asset pass) | First issue. 93 inventory rows classified by production route and **measured**, not estimated: 24 generatable (18 runnable now, 6 `BLOCKED` on the category decision), 68 vector/authored, 1 real-capture-only. Style lock and negative prompt derived from `30` §3's measured tokens. Per-row prompts with target size, ratio, intake filename and reject criteria. Three limits stated that the brief did not anticipate: no alpha channel from most models, models approximate sizes, and generated files cannot be claimed as brand-owned while `OD-COM-12` is open. `AMM-CONTROL-DENIED` carries the `03` §5 no-padlock rule; the earnings and settlement rows carry the no-financial-claim rule; two salon/beauty prompts carry the `BP-01`/`BP-02` compliance note. Intake procedure, never-generate list and traceability added. **No prompt was executed and no asset was generated in this pass; nothing here is approved.** | All |
