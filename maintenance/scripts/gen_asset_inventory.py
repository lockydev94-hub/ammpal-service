"""Generates design-assets/manifests/asset-inventory.csv from documented sources only.

Every row carries a doc_ref: the section of Docs/ that makes the asset necessary. A row with no
doc_ref is an invention and must not be added. Run from the project root.
"""
import csv, glob, os
from PIL import Image

OUT = 'design-assets/manifests/asset-inventory.csv'

COLS = ['asset_id', 'surface', 'asset_type', 'subject', 'filename_stem', 'width_px', 'height_px',
        'format', 'transparency', 'variants', 'intended_screens', 'alt_text_en', 'a11y_treatment',
        'source_class', 'generation_status', 'approval_status', 'version', 'dependencies', 'doc_ref',
        'notes']

# Accessibility treatment is declared per row, never inferred from a file extension. The four values
# are the only legal ones; validate_assets.py refuses anything else.
TREATMENT = {
    'hero': 'ALT_REQUIRED', 'illustration': 'ALT_REQUIRED', 'category-image': 'ALT_REQUIRED',
    'service-detail-image': 'ALT_REQUIRED', 'empty-state': 'ALT_REQUIRED',
    'success-state': 'ALT_REQUIRED', 'error-state': 'ALT_REQUIRED',
    'photo-placeholder': 'ALT_REQUIRED', 'logo': 'ALT_REQUIRED',
    'category-icon': 'LABELLED_BY_ADJACENT_TEXT', 'nav-icon': 'LABELLED_BY_ADJACENT_TEXT',
    'og-image': 'SOCIAL_META_IMAGE', 'feature-graphic': 'SOCIAL_META_IMAGE',
    'screenshot-set': 'NOT_SHIPPED', 'infographic': 'NOT_SHIPPED',
}

rows = []


def add(**kw):
    r = {c: kw.get(c, '') for c in COLS}
    if not r['generation_status']:
        r['generation_status'] = 'PLANNED'
    if not r['approval_status']:
        r['approval_status'] = 'NOT_APPROVED'
    if not r['version']:
        r['version'] = 'v01'
    if not r['variants']:
        r['variants'] = 'none'
    if not r['transparency']:
        r['transparency'] = 'no'
    if not r['source_class']:
        r['source_class'] = 'GENERATED_OR_SOURCED - undetermined'
    treat = TREATMENT.get(r['asset_type'], 'DECORATIVE_EMPTY_ALT')
    r['a11y_treatment'] = treat
    if treat != 'ALT_REQUIRED':
        r['alt_text_en'] = ''
    rows.append(r)


# ---------------------------------------------------------------- brand (30 sec 9, 12 sec 6.1)
BRAND = [
    ('AMM-BRAND-LOGO-HORIZONTAL', 'logo', 'horizontal lockup', 1200, 300, 'svg+png', 'yes',
     'light;dark;on-dark', 'Web app bar; email header; store listing', '12 sec 2.1 Home; 16 sec 5.2 www bundle'),
    ('AMM-BRAND-LOGO-COMPACT', 'logo', 'compact square lockup', 600, 600, 'svg+png', 'yes',
     'light;dark', 'App bar (mobile); favicon fallback', '12 sec 3.1 bottom tabs'),
    ('AMM-BRAND-MARK-MONOGRAM', 'mark', 'mark only', 512, 512, 'svg', 'yes',
     'light;dark;single-colour', 'Loading state; avatar fallback', '12 sec 6.2 Avatar'),
    ('AMM-BRAND-APPICON-MASTER', 'app-icon', 'platform icon master', 1024, 1024, 'png', 'no',
     'android-adaptive;ios', 'Device home screen', '12 sec 1 surfaces (2 Flutter apps)'),
    ('AMM-BRAND-FAVICON-SVG', 'favicon', 'scalable favicon', 0, 0, 'svg', 'yes',
     'light;dark', 'Browser tab', '12 sec 2 IA - website'),
    ('AMM-BRAND-FAVICON-PNG', 'favicon', 'raster favicon ladder', 512, 512, 'png', 'yes',
     '16;32;48;180;192;512', 'Browser tab; iOS home screen; PWA', '16 sec 5.2 static web bundle'),
    ('AMM-BRAND-OG-HOMEPAGE', 'og-image', 'link preview', 1200, 630, 'png+webp', 'no',
     'none', 'Share preview on WhatsApp (11 sec 3)', '11 sec 3 WhatsApp templates'),
    ('AMM-BRAND-PATTERN-BACKGROUND', 'pattern', 'background pattern', 1600, 1600, 'svg', 'yes',
     'light;dark', 'Web hero; email; empty states', '12 sec 6.1 foundations'),
    ('AMM-BRAND-EMAIL-LOGO', 'logo', 'email header logo', 600, 150, 'png', 'yes',
     'light', 'Email header (11 sec notifications)', '11 sec 3 notification channels'),
]
for aid, t, subj, w, h, fmt, tr, var, scr, ref in BRAND:
    add(asset_id=aid, surface='BRAND', asset_type=t, subject=subj, filename_stem=aid,
        width_px=w, height_px=h, format=fmt, transparency=tr, variants=var, intended_screens=scr,
        alt_text_en='AmmPal Service logo' if t == 'logo' else '', doc_ref=ref,
        notes='BLOCKED on OD-COM-12 (design-asset IP undecided) and OD-DOC-30 (palette unapproved)')

# ------------------------------------------------- category artwork (06 sec 4, 12 sec 3 screen 4)
LAUNCH_CATEGORIES = [
    ('APPLIANCE_REPAIR', 'appliance repair'),
    ('CLEANING', 'cleaning'),
    ('HOME_SALON', 'home salon'),
    ('BEAUTY_PARLOUR', 'beauty parlour'),
    ('PLUMBING', 'plumbing'),
    ('ELECTRICAL', 'electrical'),
]
for code, name in LAUNCH_CATEGORIES:
    slug = code.replace('_', '-')  # filenames are kebab-case; catalogue codes stay UPPER_SNAKE
    add(asset_id='AMM-SERVICE-%s-ICON-24' % slug, surface='SERVICE', asset_type='category-icon',
        subject='%s category icon' % name, filename_stem='AMM-SERVICE-%s-ICON-24' % slug,
        width_px=24, height_px=24, format='svg', transparency='yes', variants='light;dark',
        intended_screens='WEB category tiles; CUS-04 category list; CUS-02 category rail',
        alt_text_en='%s services' % name.capitalize(), source_class='ICON_LIBRARY (outline set)',
        doc_ref='12 sec 3 screen 4 "Icons, names (localised)"; 12 sec 6.1 iconography; 06 sec 4',
        notes='12 specifies ICONS for category tiles, not photographs - see OD-DOC-25. '
              'HOME_SALON/BEAUTY_PARLOUR are launch-in-06 vs Phase-4-in-17: OD-DOC-28')
    add(asset_id='AMM-SERVICE-%s-CATEGORY-800' % slug, surface='SERVICE',
        asset_type='category-image', subject='%s category image' % name,
        filename_stem='AMM-SERVICE-%s-CATEGORY-800' % slug,
        width_px=800, height_px=800, format='webp+png', transparency='no', variants='light;dark',
        intended_screens='WEB /services/{categorySlug} header; CUS-06 service detail',
        alt_text_en='%s service' % name.capitalize(),
        generation_status='BLOCKED', doc_ref='06 sec 4 launch catalogue',
        notes='BLOCKED on OD-DOC-25 (does the catalogue carry photography at all) and OD-DOC-26 '
              '(no media column on categories/services in 09)')

# ---------------------------------------------- website (12 sec 2 / 2.1, 08 sec 6.3, 12 sec 9)
add(asset_id='AMM-WEB-HERO-HOMEPAGE-1600', surface='WEB', asset_type='hero', subject='homepage hero',
    filename_stem='AMM-WEB-HERO-HOMEPAGE-1600', width_px=1600, height_px=1000, format='webp+avif+png',
    transparency='no', variants='desktop-1600;mobile-780;light', intended_screens='WEB Home',
    alt_text_en='Technician servicing a home appliance in an Indian home', source_class='PHOTOGRAPHY',
    generation_status='GENERATED', version='v02',
    doc_ref='12 sec 2.1 Home; 12 sec 9 LCP < 2.5 s on mid-range Android over 4G',
    notes='Byte budget <= 150 KB for the mobile crop; 2 MB reference PNGs in '
          'visualize-image-of-project are NOT web-fit (measured 1.88-2.12 MB). GENERATED 2026-10-22 '
          'by ChatGPT - master PNG at design-assets/02-website/masters/, optimised exports at '
          '.../exports/. v02 is the shipped master by owner choice (2026-10-22): the two versions are '
          'both on disk and v01 stays as the rejected attempt, not as a deliverable. Still NOT_APPROVED: '
          'approval is an owner act (32 sec 6, DEC-03).')
add(asset_id='AMM-WEB-OG-PARTNER-1200', surface='WEB', asset_type='og-image',
    subject='partner landing preview', filename_stem='AMM-WEB-OG-PARTNER-1200', width_px=1200,
    height_px=630, format='png+webp', intended_screens='WEB /partner', doc_ref='12 sec 2 IA /partner')
add(asset_id='AMM-WEB-ILLU-SERVICEABILITY-800', surface='WEB', asset_type='illustration',
    subject='not serviceable in your area', filename_stem='AMM-WEB-ILLU-SERVICEABILITY-800',
    width_px=800, height_px=600, format='svg', transparency='yes', variants='light',
    intended_screens='WEB /services (no coverage); CUS-03 location picker',
    alt_text_en='No technicians available in this area yet', source_class='ILLUSTRATION',
    doc_ref='23 sec 5 serviceability resolution (ADR-004); 12 sec 2.1 availability badge')
add(asset_id='AMM-WEB-PLACEHOLDER-PARTNER-512', surface='WEB', asset_type='photo-placeholder',
    subject='partner photo placeholder', filename_stem='AMM-WEB-PLACEHOLDER-PARTNER-512',
    width_px=512, height_px=512, format='webp+png', variants='light',
    intended_screens='WEB technician list/profile; CUS-08 technician profile',
    alt_text_en='Photo not yet provided', source_class='ILLUSTRATION',
    doc_ref='01 FR-CAT-05 technician card shows photo; 09 sec 4.4 technicians.photo_url',
    notes='Must never depict an identifiable person as a registered partner')

# ---------------------- website section artwork (12 sec 2.1 elements; slots sized by 39 sec 3/6)
# These twelve rows are the marketing-site artwork the owner approved for registration on 2026-10-22.
# Scope follows the same direction: the site being designed sells home appliance repair, so every
# subject is an appliance, a booking step or a support object - the cleaning/salon/plumbing imagery
# stays where it is (the six BLOCKED SERVICE rows in maintenance/holding-blocked/).
# Tiles and step cards are 4:3 at 800x600 because that is the ratio the reserved container holds
# (30 sec 5.3 says category tile 4:3; 32 sec 3 and the older 800x800 rows say 1:1 - the conflict is
# recorded in 39 sec 6 rather than resolved here).
WEB_SECTIONS = [
    ('AC-REPAIR', 'air conditioner repair', 'split air-conditioner indoor unit on a pale wall',
     'Air conditioner repair', '12 sec 2.1 Home service categories; 12 sec 2.1 /services'),
    ('FRIDGE-REPAIR', 'refrigerator repair', 'two-door refrigerator with the doors closed',
     'Refrigerator repair', '12 sec 2.1 Home service categories; 12 sec 2.1 /services'),
    ('WASHING-MACHINE-REPAIR', 'washing machine repair', 'front-load washing machine',
     'Washing machine repair', '12 sec 2.1 Home service categories; 12 sec 2.1 /services'),
    ('MICROWAVE-REPAIR', 'microwave oven repair', 'countertop microwave',
     'Microwave oven repair', '12 sec 2.1 Home service categories; 12 sec 2.1 /services'),
    ('WATER-PURIFIER-REPAIR', 'water purifier repair',
     'under-sink water purifier with one visible filter cartridge', 'Water purifier repair',
     '12 sec 2.1 Home service categories; 12 sec 2.1 /services'),
    ('STEP-SEARCH', 'how it works step 1', 'a plain house roofline with a soft rounded search ring',
     'Tell us the appliance and your area', '12 sec 2.1 Home how-it-works; 12 sec 2.1 /services'),
    ('STEP-SLOT', 'how it works step 2', 'a blank calendar card with one chosen space marked',
     'Choose a time that suits you', '12 sec 2.1 Home how-it-works; 23 sec 11 slot availability'),
    ('STEP-VISIT', 'how it works step 3', 'a service toolbox on a folded mat before a closed door',
     'A service toolbox resting on a floor mat in front of a closed door',
     '12 sec 2.1 Home how-it-works; 12 sec 3.11 technician visit'),
]
for slug, subj, desc, alt, ref in WEB_SECTIONS:
    add(asset_id='AMM-WEB-ILLU-%s-800' % slug, surface='WEB', asset_type='illustration',
        subject=subj, filename_stem='AMM-WEB-ILLU-%s-800' % slug, width_px=800, height_px=600,
        format='svg', transparency='yes', variants='light',
        intended_screens='WEB Home section grid; WEB /services tiles' if 'REPAIR' in slug
        else 'WEB Home how-it-works steps',
        alt_text_en=alt, source_class='ILLUSTRATION', doc_ref=ref,
        notes='%s. One flat two-fill-plus-accent drawing on #FFFFFF from the 39 prompt pack - the five '
              'appliance tiles and the three step cards must read as one family (same camera height, '
              'same object scale, same ground). Ships as traced SVG; a raster export is the '
              'design-time placeholder (30 sec 11, 32 sec 4 ceiling 12 KB). Generated != owned while '
              'OD-COM-12 is open.' % desc)

for slug, subj, desc, alt, ref in [
    ('TRUST-VERIFIED', 'trust signals band',
     'a screwdriver and a spanner laid side by side on a folded service cloth',
     "A technician's tools laid out ready for a visit",
     '12 sec 2.1 Home trust signals; 12 sec 2.1 /about'),
    ('PRICING-TRANSPARENT', 'price transparency',
     'a plain estimate sheet with three blank bands beside it',
     'An estimate sheet with three blank bands beside it',
     '12 sec 2.1 /pricing; 00 FR-01/FR-03 price snapshot'),
    ('SUPPORT-HELPLINE', 'support helpline',
     'a desk telephone handset in its cradle beside a closed notebook',
     'A desk telephone handset resting in its cradle beside a closed notebook',
     '12 sec 2.1 /support; 05 sec 3 toll-free contact'),
]:
    add(asset_id='AMM-WEB-ILLU-%s-800' % slug, surface='WEB', asset_type='illustration',
        subject=subj, filename_stem='AMM-WEB-ILLU-%s-800' % slug, width_px=800, height_px=600,
        format='svg', transparency='yes', variants='light',
        intended_screens='WEB Home %s; WEB /%s' % (subj, 'pricing' if slug == 'PRICING-TRANSPARENT'
        else 'support' if slug == 'SUPPORT-HELPLINE' else 'about'),
        alt_text_en=alt, source_class='ILLUSTRATION', doc_ref=ref,
        notes='%s. The alt describes the drawing and asserts nothing: verification, a price and the '
              'toll-free number are data rendered as interface text, never artwork (34 sec 7, DD-06). '
              'Reject if a badge, seal, star, shield, figure, currency mark or phone number appears in '
              'the pixels. Ships as traced SVG; raster is the placeholder (30 sec 11, 32 sec 4).' % desc)

add(asset_id='AMM-WEB-HERO-PARTNER-1600', surface='WEB', asset_type='hero',
    subject='partner landing hero', filename_stem='AMM-WEB-HERO-PARTNER-1600', width_px=1600,
    height_px=1000, format='webp+avif+png', transparency='no',
    variants='desktop-1600;mobile-780;light', intended_screens='WEB /partner',
    alt_text_en='Work with AmmPal Service as a technician or a partner branch',
    source_class='ILLUSTRATION',
    doc_ref='12 sec 2 IA /partner; 12 sec 2.1 /partner key elements; 26 sec 4.1 partner claims',
    notes='At most four unmarked objects (toolbox, rolled cloth, screwdriver, split A/C unit) with the '
          'left half of the frame kept as empty pale space for the headline, which is interface text. '
          'No earnings, payout date or partner-count claim may be drawn into it - 26 sec 4.1 and '
          '34 sec 7 both refuse invented commercial claims. Ceiling 150 KB on the mobile crop '
          '(32 sec 4).')

# ---------------------------------------------- customer app empty/success (12 sec 3.2 screens)
CUST_EMPTY = [
    ('BOOKINGS', 'no bookings yet', 'CUS-14 booking list (all tabs)'),
    ('NOTIFICATIONS', 'no notifications', 'CUS-23 notifications'),
    ('SUPPORT', 'no tickets', 'CUS-24 support'),
    ('SLOTS', 'no slots available', 'CUS-09 slot picker'),
    ('TECHNICIANS', 'no technicians available', 'CUS-07 technician list'),
]
for subj, alt, scr in CUST_EMPTY:
    add(asset_id='AMM-CUSTOMER-EMPTY-%s-600' % subj, surface='CUSTOMER', asset_type='empty-state',
        subject='%s empty state' % subj.lower(), filename_stem='AMM-CUSTOMER-EMPTY-%s-600' % subj,
        width_px=600, height_px=450, format='svg', transparency='yes', variants='light',
        intended_screens=scr, alt_text_en=alt, source_class='ILLUSTRATION', doc_ref='12 sec 3.2')
add(asset_id='AMM-CUSTOMER-SUCCESS-BOOKING-600', surface='CUSTOMER', asset_type='success-state',
    subject='booking confirmed', filename_stem='AMM-CUSTOMER-SUCCESS-BOOKING-600', width_px=600,
    height_px=600, format='svg', transparency='yes', variants='light',
    intended_screens='CUS-13 booking confirmation; CUS-20 payment success', alt_text_en='Booking confirmed',
    source_class='ILLUSTRATION', doc_ref='12 sec 3.2 screens 13 and 20',
    notes='No celebratory loop that could be read as proof of server state - 30 sec 7, '
          'and payment success must reflect a confirmed gateway state (23 sec 11.2)')

# ---------------------------------------------- partner app empty (12 sec 4.2 screens)
PARTNER_EMPTY = [
    ('JOBS', 'no offers right now', 'PAR-03 job feed'),
    ('EARNINGS', 'no earnings yet', 'PAR-12 earnings; PAR-13 earnings detail'),
    ('SETTLEMENT', 'no statements yet', 'PAR-14 settlement statement'),
    ('CALENDAR', 'no scheduled jobs', 'PAR-16 calendar'),
]
for subj, alt, scr in PARTNER_EMPTY:
    add(asset_id='AMM-PARTNER-EMPTY-%s-480' % subj, surface='PARTNER', asset_type='empty-state',
        subject='%s empty state' % subj.lower(), filename_stem='AMM-PARTNER-EMPTY-%s-480' % subj,
        width_px=480, height_px=360, format='svg', transparency='yes', variants='light',
        intended_screens=scr, alt_text_en=alt, source_class='ILLUSTRATION', doc_ref='12 sec 4.2')

# ------------------------------------ Control Center: nav icons generated from 12 sec 5.1 tree
CC_NAV = """Overview|overview
Bookings|bookings
Job Feed|job-feed
Assignments|assignments
Technicians|technicians
Coverage|coverage
SLA Monitor|sla-monitor
Partner Orgs|partner-orgs
Branches|branches
Territory|territory
Technician KYC|technician-kyc
Approvals Queue|approvals-queue
Categories|categories
Services and Variants|services-variants
Workflow Templates|workflow-templates
Price Book|price-book
Branch Prices|branch-prices
Coupons|coupons
Commission Rates|commission-rates
Commission Ledger|commission-ledger
Settlements|settlements
Invoices|invoices
Reconciliation|reconciliation
Adjustments and Disputes|adjustments-disputes
Tax Registrations|tax-registrations
Partner Payouts|partner-payouts
Call Console|call-console
Ticket Queue|ticket-queue
Escalations|escalations
Complaints|complaints
CSAT and QA|csat-qa
Campaigns|campaigns
Offers|offers
Content|content
Funnel and Conversion|funnel-conversion
Revenue and Margin|revenue-margin
Technician Performance|technician-performance
Branch P and L|branch-pl
Exports|exports
Users and Roles|users-roles
Audit Log|audit-log
Feature Flags|feature-flags
Master Data|master-data"""
for line in CC_NAV.splitlines():
    label, slug = line.split('|')
    add(asset_id='AMM-CONTROL-ICON-%s-24' % slug.upper(), surface='CONTROL', asset_type='nav-icon',
        subject='%s navigation icon' % label, filename_stem='AMM-CONTROL-ICON-%s-24' % slug.upper(),
        width_px=24, height_px=24, format='svg', transparency='yes',
        variants='default;active;focus', intended_screens='CC sidebar: %s' % label,
        alt_text_en='', source_class='ICON_LIBRARY (outline set)', doc_ref='12 sec 5.1 navigation tree',
        notes='Role-filtered visibility comes from 03 sec 4; the icon itself is not a permission cue')

add(asset_id='AMM-CONTROL-EMPTY-TABLE-480', surface='CONTROL', asset_type='empty-state',
    subject='empty table', filename_stem='AMM-CONTROL-EMPTY-TABLE-480', width_px=480, height_px=360,
    format='svg', transparency='yes', variants='light',
    intended_screens='All CC DataTables (12 sec 6.2)', alt_text_en='No records match this filter',
    source_class='ILLUSTRATION', doc_ref='12 sec 6.2 DataTable, EmptyState')
add(asset_id='AMM-CONTROL-DENIED-600', surface='CONTROL', asset_type='error-state',
    subject='permission denied', filename_stem='AMM-CONTROL-DENIED-600', width_px=600, height_px=450,
    format='svg', transparency='yes', variants='light', intended_screens='Any scope-denied CC screen',
    alt_text_en='You do not have access to this data', source_class='ILLUSTRATION',
    doc_ref='03 sec 5 step 3 (404 not 403); 12 sec 5.1 scope-aware navigation',
    notes='Out-of-scope reads return 404, never 403 (03 sec 5 step 3 - resource existence is not '
          'leaked), so the state must read "not found" rather than "you cannot see this"')
for marker, meaning in [('TECHNICIAN', 'technician live position'), ('JOB', 'booking job site'),
                       ('ZONE', 'service-area boundary'), ('PICKUP', 'customer pin')]:
    add(asset_id='AMM-CONTROL-MARKER-%s-32' % marker, surface='CONTROL', asset_type='map-marker',
        subject='%s map marker' % meaning, filename_stem='AMM-CONTROL-MARKER-%s-32' % marker,
        width_px=32, height_px=40, format='svg', transparency='yes',
        variants='default;selected;cluster', intended_screens='CUS-16 live tracking; CC coverage board',
        alt_text_en='', source_class='ILLUSTRATION',
        doc_ref='12 sec 6.2 MapPicker; 13 sec 5.2 CSP img-src maps.googleapis.com; 09 PostGIS',
        notes='Rendered on Google Maps (CSP allows only maps.googleapis.com/gstatic/usercontent) - '
              'not a PostGIS tile layer; must be validated against the real map SDK (30 sec 8)')

# ---------------------------------------------- store and PWA (12 sec 1, 29 sec 4)
add(asset_id='AMM-STORE-PLAY-ICON-512', surface='STORE', asset_type='store-icon',
    subject='Google Play icon', filename_stem='AMM-STORE-PLAY-ICON-512', width_px=512, height_px=512,
    format='png', transparency='no', variants='none', intended_screens='Play Store listing',
    source_class='DERIVED from AMM-BRAND-APPICON-MASTER', doc_ref='12 sec 1 surfaces',
    notes='Re-verify against the official Play spec at submission time - specs change')
add(asset_id='AMM-STORE-PLAY-FEATURE-1024', surface='STORE', asset_type='feature-graphic',
    subject='Play feature graphic', filename_stem='AMM-STORE-PLAY-FEATURE-1024', width_px=1024,
    height_px=500, format='png', intended_screens='Play Store listing', source_class='PHOTOGRAPHY+TYPE',
    doc_ref='12 sec 1 surfaces', notes='No rating, "verified", or guarantee claim that 26 does not authorise')
for size in (192, 512):
    add(asset_id='AMM-WEB-PWA-ICON-%d' % size, surface='WEB', asset_type='pwa-icon',
        subject='PWA icon %d' % size, filename_stem='AMM-WEB-PWA-ICON-%d' % size, width_px=size,
        height_px=size, format='png', intended_screens='PWA install (website)',
        source_class='DERIVED from AMM-BRAND-APPICON-MASTER', doc_ref='12 sec 2 IA - website')
add(asset_id='AMM-STORE-SCREENSHOTS-SET', surface='STORE', asset_type='screenshot-set',
    subject='store screenshots', filename_stem='AMM-STORE-SCREENSHOTS', width_px=0, height_px=0,
    format='png', variants='en;or;hi', intended_screens='Play Store listing',
    source_class='REAL_APP_CAPTURE', doc_ref='12 sec 1 surfaces',
    notes='Cannot start yet rather than blocked by a decision: must be captured from approved running '
          'screens and nothing is implemented (README sec 4.1). No simulated screenshot is permitted')

# ---------------------------------------------- reference register (existing, read-only)
REFS = [('AMM-REF-ARCH-INFONODE', 'AmmPal Service Architecture Infographic.png', 1536, 1024, '94bf8ef8e966c2a3'),
        ('AMM-REF-CALL-FLOW', 'AmmPal Service Call Support Workflow.png', 1536, 1024, '2d087d4f2609dd7d'),
        ('AMM-REF-E2E-FLOW', 'AmmPal Service End-to-End Workflow.png', 1536, 1024, 'bd9d956edd53a12e'),
        ('AMM-REF-PRICING-FLOW', 'AmmPal Service Pricing Workflow Infographic.png', 1536, 1024, '598ac375329c8cb1')]
for aid, fn, w, h, digest in REFS:
    add(asset_id=aid, surface='REFERENCE', asset_type='infographic', subject=fn,
        filename_stem=fn, width_px=w, height_px=h, format='png', generation_status='REGISTERED',
        approval_status='NOT_FOR_PRODUCTION', source_class='THIRD_PARTY_AI (ChatGPT) - prompt, model and '
        'licence unrecorded; filesystem mtime 2026-10-12',
        intended_screens='Internal reference only', doc_ref='visualize-image-of-project/',
        dependencies='sha256:%s' % digest,
        notes='Reference only. Not a brand asset, not web-sized, and not reusable in product UI until '
              'OD-COM-12 settles design-asset IP')

# --------------------------------------------------- generation status is derived from disk
# A row reads GENERATED only if its master file actually exists in that section's masters/ directory,
# so the register cannot claim an asset it cannot point at, and re-running this script after an intake
# is the whole write-back. BLOCKED rows are never flipped here: Docs/32 sec 6 says a BLOCKED row cannot
# enter GENERATED, so a generated file for one belongs in maintenance/holding-blocked, not in
# design-assets/. approval_status stays NOT_APPROVED in every case - approval is an owner act (DEC-03).
SURFACE_DIR = {'BRAND': '01-brand', 'WEB': '02-website', 'CUSTOMER': '03-customer-app',
               'PARTNER': '04-partner-app', 'CONTROL': '05-control-center', 'STORE': '08-store',
               'SERVICE': '09-service-catalogue'}

for r in rows:
    section = SURFACE_DIR.get(r['surface'])
    if not section or r['generation_status'] != 'PLANNED':
        continue
    found = sorted(glob.glob('design-assets/%s/masters/%s-v*.png' % (section, r['filename_stem'])))
    if not found:
        continue
    newest = found[-1]
    with Image.open(newest) as im:  # measured, never asserted (Docs/32 sec 3)
        mw, mh = im.size
    r['generation_status'] = 'GENERATED'
    r['version'] = 'v' + os.path.basename(newest).rsplit('-v', 1)[1][:2]
    r['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + (
        'GENERATED 2026-10-22 by ChatGPT from a maintenance/prompts/ block. Master %s measured %dx%d; '
        'exports regenerable with maintenance/scripts/intake_asset.py. NOT_APPROVED: approval is an '
        'owner act (32 sec 6, DEC-03).' % (newest.replace('\\', '/'), mw, mh))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    # lineterminator is explicit because csv.writer defaults to CRLF while the committed register is
    # LF, and .gitattributes carries `* -text` (no EOL normalisation) - without this, every run on
    # Windows rewrites all 94 lines and the register diff hides the one row that actually changed.
    wtr = csv.DictWriter(fh, fieldnames=COLS, lineterminator='\n')
    wtr.writeheader()
    wtr.writerows(rows)

by_status = {}
by_type = {}
for r in rows:
    by_status[r['generation_status']] = by_status.get(r['generation_status'], 0) + 1
    by_type[r['surface']] = by_type.get(r['surface'], 0) + 1
print('rows', len(rows))
print('by status', by_status)
print('by surface', by_type)
