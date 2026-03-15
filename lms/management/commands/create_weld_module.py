from django.core.management.base import BaseCommand

from lms.models import Tier, Module, Lesson, InteractiveExercise


class Command(BaseCommand):
    help = 'Create Module 3 — Weld Quality and Documentation'

    def handle(self, *args, **options):
        tier = Tier.objects.get(slug='practitioner')

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # MODULE 3 — Weld Quality and Documentation (gated)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        mod3, mod3_created = Module.objects.get_or_create(
            tier=tier, order=3,
            defaults={
                'title': 'Weld Quality and Documentation',
                'gate_required': True,
            },
        )
        if not mod3.gate_required:
            mod3.gate_required = True
            mod3.save()
        self.stdout.write(
            f'Module 3: {"created" if mod3_created else "found"} — '
            f'{mod3.title} [GATED]'
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LESSONS 10–15
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── Lesson 10 ──
        Lesson.objects.get_or_create(
            module=mod3, order=10,
            defaults={
                'title': 'Reading a Welding Procedure Specification',
                'content_type': 'reading',
                'estimated_minutes': 8,
                'body': (
                    '<p>A Welding Procedure Specification (WPS) is the governing document '
                    'for every weld made on a pipeline or piping system. Before the arc '
                    'is struck, the WPS must be posted at the work location, verified as '
                    'applicable to the joint being welded, and understood by the welder '
                    'performing the work. A WPS that is not read is not being followed \u2014 '
                    'and a weld made outside the WPS is nonconforming regardless of how '
                    'it looks.</p>'

                    '<p>The WPS defines every essential and non-essential variable that '
                    'controls weld quality. Essential variables are those whose change '
                    'requires requalification: base material P-number or group, filler '
                    'metal classification, welding process, preheat and interpass '
                    'temperature limits, position, joint design, and post-weld heat '
                    'treatment. Non-essential variables can be changed with a WPS '
                    'revision without requalification. Know the difference \u2014 an inspector '
                    'who cannot read a WPS cannot determine whether a weld is in '
                    'compliance.</p>'

                    '<p>The most common field errors with WPS compliance are position '
                    'violations and filler metal substitutions. A welder qualified in the '
                    '1G (flat) position only cannot legally weld a 5G (horizontal fixed) '
                    'joint, even if they are physically capable of doing so. Similarly, '
                    'substituting E7018-H4 for E7018 without a WPS revision or '
                    'engineering approval is a nonconformance \u2014 different hydrogen '
                    'designators are not interchangeable under most codes. When in doubt, '
                    'stop and verify with the QC Inspector before proceeding.</p>'

                    '<p>For API 1104 pipeline work, the WPS must also specify the pipe '
                    'grade, wall thickness range, and OD range covered. A WPS qualified '
                    'on 0.375" wall does not automatically cover 0.500" wall without '
                    'requalification data supporting that range. Check the essential '
                    'variable ranges on the front page of the WPS against the actual pipe '
                    'being welded before every new joint configuration begins. This takes '
                    'two minutes and prevents a rejected weld that takes two days to '
                    'resolve.</p>'
                ),
            },
        )

        # ── Lesson 11 ──
        Lesson.objects.get_or_create(
            module=mod3, order=11,
            defaults={
                'title': 'Welder Qualification and What It Means in the Field',
                'content_type': 'reading',
                'estimated_minutes': 7,
                'body': (
                    '<p>A Welder Qualification Record (WQR) \u2014 sometimes called a Welder '
                    'Performance Qualification (WPQ) \u2014 documents that a specific welder '
                    'has demonstrated the ability to produce acceptable welds under the '
                    'conditions defined by the qualifying test. The WQR is not a '
                    'certification of the welder as a person; it is a record of a '
                    'specific test made under specific conditions. A welder\u2019s '
                    'qualifications can expire, can be voided by extended inactivity, '
                    'and may not cover the joint configuration in front of them even if '
                    'they have been welding for twenty years.</p>'

                    '<p>Before any welder picks up a stinger on your job, verify three '
                    'things: their WQR is current and on file, the process and position '
                    'on the WQR covers the work being performed, and the base material '
                    'and filler classification on the WQR match or are within the '
                    'essential variable limits of the active WPS. A welder stamp or ID '
                    'number is how you connect the weld to the record. Every joint on the '
                    'weld log must show the welder stamp for the person who made that weld '
                    '\u2014 not the crew lead, not the foreman, the actual welder.</p>'

                    '<p>Continuity is a frequently overlooked qualification issue on long '
                    'pipeline projects. Under API 1104 Section 6.4, a welder who has not '
                    'welded with a given process for six months or more has their '
                    'qualification lapse for that process. On a project where welders '
                    'rotate in and out, it is the QC Inspector\u2019s responsibility to track '
                    'continuity status and flag lapses before welding begins, not after. '
                    'A weld made by a welder whose qualification has lapsed is '
                    'nonconforming and requires either acceptance by engineering '
                    'disposition or removal and replacement.</p>'

                    '<p>Welder stamps are the traceability link between the physical weld '
                    'and the qualification record. On compressor station and pipeline '
                    'tie-in work, stamps are typically a two to four digit alphanumeric '
                    'code unique to each welder on the project. The stamp goes on the '
                    'pipe adjacent to the weld at the time of completion \u2014 not days '
                    'later. If a weld cannot be traced to a welder stamp, it cannot be '
                    'accepted without additional NDE and documentation to establish '
                    'identity and qualification coverage.</p>'
                ),
            },
        )

        # ── Lesson 12 ──
        Lesson.objects.get_or_create(
            module=mod3, order=12,
            defaults={
                'title': 'Joint Fit-Up and Pre-Weld Inspection',
                'content_type': 'reading',
                'estimated_minutes': 8,
                'body': (
                    '<p>Pre-weld inspection is the highest-leverage quality activity on '
                    'any pipeline or piping job. A joint that is set up correctly \u2014 '
                    'proper fit-up, verified preheat, correct filler metal staged \u2014 '
                    'produces a good weld. A joint with poor fit-up, insufficient '
                    'preheat, or the wrong electrode produces a defect that will require '
                    'repair or replacement. The QC Inspector\u2019s job at the pre-weld stage '
                    'is to prevent defects, not to document them after the fact.</p>'

                    '<p>Fit-up verification covers four items: root opening, land (root '
                    'face) dimension, bevel angle, and pipe alignment (hi-lo). The WPS '
                    'and project specification define the acceptable range for each. '
                    'Typical values for SMAW pipeline work are a root opening of 1/16" '
                    'to 3/32", a land of 1/16" \u00b1 1/32", a bevel of 30\u00b0 \u00b1 2.5\u00b0 per side, '
                    'and a maximum hi-lo (internal misalignment) of 1/8" or 10% of wall '
                    'thickness, whichever is less. Any fit-up outside these ranges shall '
                    'be corrected before welding begins. Correcting fit-up after the root '
                    'pass is exponentially more expensive than correcting it before.</p>'

                    '<p>Preheat is not optional on carbon steel in pipeline service. For '
                    'API 5L X65 pipe with wall thicknesses up to 0.500", the minimum '
                    'preheat temperature is typically 100\u00b0F (38\u00b0C). For heavier walls, '
                    'high-restraint joints, or ambient temperatures below 40\u00b0F, preheat '
                    'requirements increase. Preheat shall be verified with a calibrated '
                    'temperature-indicating device \u2014 temperature-indicating sticks '
                    '(Tempilstik) or infrared thermometers \u2014 within one inch of the joint '
                    'on both sides immediately before welding begins. Recording a preheat '
                    'temperature on the traveler without measuring it is falsification of '
                    'a quality record.</p>'

                    '<p>Cleanliness is the final pre-weld check. The joint bevel and the '
                    'adjacent pipe surface (minimum 1" each side) shall be free of mill '
                    'scale, rust, paint, moisture, oil, and debris. Any organic '
                    'contamination is a potential hydrogen source and a porosity risk. If '
                    'weather conditions create a condensation risk on the pipe, the joint '
                    'shall be preheated above the dew point before welding begins. '
                    'Document all pre-weld conditions on the joint traveler before the '
                    'root pass is started \u2014 once welding begins, the pre-weld record '
                    'cannot be reconstructed.</p>'
                ),
            },
        )

        # ── Lesson 13 ──
        Lesson.objects.get_or_create(
            module=mod3, order=13,
            defaults={
                'title': 'In-Process and Final Visual Weld Inspection',
                'content_type': 'reading',
                'estimated_minutes': 7,
                'body': (
                    '<p>Visual inspection during welding is as important as the final '
                    'visual after completion. The root pass is the most critical pass in '
                    'any groove weld \u2014 it sets the profile of the joint, establishes '
                    'fusion at the root, and in pipeline work is the pass most '
                    'susceptible to burnthrough, incomplete penetration, and root '
                    'concavity. The QC Inspector should observe the root pass when '
                    'practicable and verify root pass appearance before fill passes begin. '
                    'A bad root that is covered with fill is a defect that cannot be '
                    'visually detected after the fact and must go to NDE.</p>'

                    '<p>Interpass temperature is a continuous in-process requirement. The '
                    'maximum interpass temperature limits the heat input into the joint '
                    'and controls the heat-affected zone properties. For most X65 carbon '
                    'steel pipeline work, the maximum interpass temperature is 400\u00b0F '
                    '(204\u00b0C). If the interpass temperature exceeds this limit, welding '
                    'shall stop and the joint shall be allowed to cool before the next '
                    'pass is deposited. Record the interpass temperature measurement on '
                    'the traveler \u2014 it is an essential variable under the WPS and must '
                    'be documented.</p>'

                    '<p>Final visual inspection of completed welds covers surface '
                    'condition, weld profile, and dimensional requirements. Under API '
                    '1104, the weld face shall be free of cracks, incomplete fusion '
                    'visible at the surface, surface porosity exceeding the code limit, '
                    'and undercut exceeding 1/32" depth or 12.5% of wall thickness. '
                    'Reinforcement (crown height) shall not exceed 1/8" above the pipe '
                    'OD surface. Underfill \u2014 where the weld face is below the pipe '
                    'surface \u2014 is rejectable without a fitness-for-service evaluation. '
                    'Record all observations with specific measurements where rejectable '
                    'conditions are found or suspected.</p>'

                    '<p>Every completed weld shall be dispositioned as ACC or REJ based '
                    'on the applicable acceptance criteria. A visual accept does not mean '
                    'NDE accept \u2014 visual and NDE are separate inspection activities with '
                    'separate disposition columns on the weld log. Do not conflate them. '
                    'A weld that passes visual but fails radiography is REJ until repaired '
                    'and re-examined. The final disposition recorded on the weld traveler '
                    'shall reflect all applicable inspection results, not just the last '
                    'one performed.</p>'
                ),
            },
        )

        # ── Lesson 14 ──
        Lesson.objects.get_or_create(
            module=mod3, order=14,
            defaults={
                'title': 'Weld Documentation and Traveler Management',
                'content_type': 'reading',
                'estimated_minutes': 6,
                'body': (
                    '<p>The weld traveler is the complete quality record for a single weld '
                    'joint. It follows the joint from fit-up through final NDE, and it is '
                    'the document that proves to the owner, the regulator, and the test '
                    'witness that the joint was produced in accordance with the applicable '
                    'code and project specification. A weld that cannot be documented is '
                    'a weld that cannot be accepted. No traveler, no turnover.</p>'

                    '<p>A complete weld traveler contains: the joint identification number '
                    'as shown on the weld map or isometric drawing; the pipe material '
                    'specification, grade, OD, and wall thickness; the WPS number and '
                    'revision; the welder stamp for each welder who contributed passes to '
                    'the joint; the filler metal classification and heat or lot number; '
                    'pre-weld preheat temperature and method of measurement; interpass '
                    'temperature high reading; NDE method, procedure number, and '
                    'technician certification level; NDE result and report number; visual '
                    'inspection result; and final disposition with the inspector\u2019s '
                    'signature and date. Missing any of these is an incomplete record.</p>'

                    '<p>The weld map assigns a unique weld identification number to every '
                    'joint on the system. The weld map number must match the traveler. If '
                    'a weld is made that does not appear on the weld map, it does not '
                    'exist in the quality record regardless of how well it is welded. '
                    'Adding welds to a system that were not captured on the weld map '
                    'during construction is one of the most common pre-turnover crises on '
                    'pipeline projects \u2014 find them during construction by auditing the '
                    'weld map against the physical system weekly.</p>'

                    '<p>Weld log closure is a daily discipline. Complete travelers daily, '
                    'not at the end of the job. A traveler filled out three weeks after '
                    'the weld was made relies on memory and reconstruction, both of which '
                    'are unreliable and neither of which satisfies the audit trail '
                    'requirement. The project QC file is only as current as the day\u2019s '
                    'traveler submissions. If the inspector\u2019s desk has a stack of open '
                    'travelers at the end of the week, quality control has already lost '
                    'ground it will struggle to recover.</p>'
                ),
            },
        )

        # ── Lesson 15 — Interactive Exercise ──
        lesson_15, l15_created = Lesson.objects.get_or_create(
            module=mod3, order=15,
            defaults={
                'title': 'Practical Exercise: Weld Inspection Log',
                'content_type': 'interactive',
                'estimated_minutes': 35,
                'body': '',
            },
        )
        if not l15_created and lesson_15.content_type != 'interactive':
            lesson_15.content_type = 'interactive'
            lesson_15.title = 'Practical Exercise: Weld Inspection Log'
            lesson_15.estimated_minutes = 35
            lesson_15.body = ''
            lesson_15.save()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # INTERACTIVE EXERCISE
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        exercise_config = {
            "exercise_type": "weld_log",
            "title": "Weld Inspection Log",
            "subtitle": "FDQ Tier 1 \u00b7 Module 3 Gate Exercise",
            "project": "Mustang Creek Compressor Station",
            "system": "Station Piping Tie-In Welds",
            "spec": "API 1104 21st Edition / ASME B31.8",
            "service": "Natural Gas \u2014 Sour Service",
            "total_steps": 5,
            "steps": [
                {
                    "id": "wps_verification",
                    "label": "Step 1 of 5 \u2014 WPS Applicability",
                    "description": "Verify WPS-CS-001 covers WLD-001 using the WPS documents",
                    "scope": "WLD-001 only",
                },
                {
                    "id": "material_traceability",
                    "label": "Step 2 of 5 \u2014 Material Traceability",
                    "description": "Verify pipe MTR, filler metal certs, and welder qualification for WLD-001",
                    "scope": "WLD-001 only",
                },
                {
                    "id": "pre_weld_fitup",
                    "label": "Step 3 of 5 \u2014 Pre-Weld & Fit-Up",
                    "description": "Record fit-up measurements and pre-weld conditions for WLD-001",
                    "scope": "WLD-001 only",
                },
                {
                    "id": "in_process_log",
                    "label": "Step 4 of 5 \u2014 In-Process Parameters",
                    "description": "Record pass-by-pass welder stamps, interpass temps, and filler metals for all joints",
                    "scope": "All 5 joints",
                },
                {
                    "id": "final_inspection",
                    "label": "Step 5 of 5 \u2014 Final Inspection & NDE",
                    "description": "Record visual results, NDE method, report numbers, and final disposition for all joints",
                    "scope": "All 5 joints",
                },
            ],
            "scenario": {
                "inspector": "T. Garza",
                "inspector_initials": "T. GARZA",
                "date": "03/14/2026",
                "shift": "Day",
                "welds": [
                    {
                        "id": "WLD-001",
                        "description": "12\" Mainline Tie-In \u2014 North End",
                        "pipe_spec": "API 5L X65",
                        "od": "12.750\"",
                        "wt": "0.375\"",
                        "position": "5G",
                        "process": "SMAW/FCAW",
                        "wps": "WPS-CS-001 Rev. 4",
                        "welder": "M. Torres",
                        "welder_stamp": "W-042",
                        "preheat_required": "100\u00b0F",
                        "preheat_measured": "125\u00b0F",
                        "preheat_method": "Tempilstik",
                        "interpass_max": "400\u00b0F",
                        "interpass_high": "325\u00b0F",
                        "root_opening": "5/64\"",
                        "hi_lo": "3/32\"",
                        "bevel_angle": "30\u00b0",
                        "land": "1/16\"",
                        "cleanliness": "PASS",
                        "passes": 4,
                        "filler_root": "E7018-H4",
                        "filler_fill": "E71T-1M-H8",
                        "crown_height": "3/32\"",
                        "undercut": "None",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-044",
                        "nde_result": "ACC",
                        "visual_result": "ACC",
                        "disposition": "ACC",
                        "remarks": "Root pass visual verified prior to fill. Full penetration confirmed. No rejectable conditions.",
                    },
                    {
                        "id": "WLD-002",
                        "description": "12\" Mainline Tie-In \u2014 South End",
                        "pipe_spec": "API 5L X65",
                        "od": "12.750\"",
                        "wt": "0.375\"",
                        "position": "5G",
                        "process": "SMAW/FCAW",
                        "wps": "WPS-CS-001 Rev. 4",
                        "welder": "D. Kimura",
                        "welder_stamp": "W-019",
                        "preheat_required": "100\u00b0F",
                        "preheat_measured": "115\u00b0F",
                        "interpass_max": "400\u00b0F",
                        "interpass_high": "310\u00b0F",
                        "passes": 4,
                        "filler_root": "E7018-H4",
                        "filler_fill": "E71T-1M-H8",
                        "crown_height": "3/32\"",
                        "undercut": "None",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-045",
                        "nde_result": "ACC",
                        "visual_result": "ACC",
                        "disposition": "ACC",
                        "remarks": "All passes within WPS limits. Crown height 3/32\". No rejectable conditions.",
                    },
                    {
                        "id": "WLD-003",
                        "description": "8\" Recycle Header Tie-In",
                        "pipe_spec": "API 5L X65",
                        "od": "8.625\"",
                        "wt": "0.322\"",
                        "position": "6G",
                        "process": "SMAW",
                        "wps": "WPS-CS-002 Rev. 2",
                        "welder": "M. Torres",
                        "welder_stamp": "W-042",
                        "preheat_required": "100\u00b0F",
                        "preheat_measured": "110\u00b0F",
                        "interpass_max": "400\u00b0F",
                        "interpass_high": "298\u00b0F",
                        "passes": 3,
                        "filler_root": "E7018-H4",
                        "filler_fill": "E7018-H4",
                        "crown_height": "1/16\"",
                        "undercut": "None",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-046",
                        "nde_result": "ACC",
                        "visual_result": "ACC",
                        "disposition": "ACC",
                        "remarks": "6G position. Full circumferential RT. No indications.",
                    },
                    {
                        "id": "WLD-004",
                        "description": "6\" PSV Discharge Tie-In",
                        "pipe_spec": "API 5L X65",
                        "od": "6.625\"",
                        "wt": "0.280\"",
                        "position": "2G",
                        "process": "SMAW",
                        "wps": "WPS-CS-002 Rev. 2",
                        "welder": "R. Castillo",
                        "welder_stamp": "W-031",
                        "preheat_required": "100\u00b0F",
                        "preheat_measured": "105\u00b0F",
                        "interpass_max": "400\u00b0F",
                        "interpass_high": "285\u00b0F",
                        "passes": 3,
                        "filler_root": "E7018-H4",
                        "filler_fill": "E7018-H4",
                        "crown_height": "1/16\"",
                        "undercut": "None",
                        "nde_method": "UT",
                        "nde_report": "UT-2026-019",
                        "nde_result": "ACC",
                        "visual_result": "ACC",
                        "disposition": "ACC",
                        "remarks": "Phased array UT per UT-PROC-007. No reportable indications.",
                    },
                    {
                        "id": "WLD-005",
                        "description": "12\" Weld Neck Flange \u2014 Discharge Header",
                        "pipe_spec": "API 5L X65 / ASTM A105N",
                        "od": "12.750\"",
                        "wt": "0.375\"",
                        "position": "5G",
                        "process": "SMAW/FCAW",
                        "wps": "WPS-CS-001 Rev. 4",
                        "welder": "D. Kimura",
                        "welder_stamp": "W-019",
                        "preheat_required": "100\u00b0F",
                        "preheat_measured": "120\u00b0F",
                        "interpass_max": "400\u00b0F",
                        "interpass_high": "318\u00b0F",
                        "passes": 4,
                        "filler_root": "E7018-H4",
                        "filler_fill": "E71T-1M-H8",
                        "crown_height": "3/32\"",
                        "undercut": "None",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-047",
                        "nde_result": "ACC",
                        "visual_result": "ACC",
                        "disposition": "ACC",
                        "remarks": "Flange-to-spool weld. Flange orientation confirmed prior to welding.",
                    },
                ],
                "wpss": [
                    {
                        "number": "WPS-CS-001 Rev. 4",
                        "process": "SMAW / FCAW-G",
                        "base_metal": "API 5L X52 through X70 / ASTM A105N",
                        "p_number": "P-1 Group 1 and 2",
                        "filler_root": "E7018-H4 (SMAW)",
                        "filler_fill_cap": "E71T-1M-H8 (FCAW-G)",
                        "positions": "1G, 2G, 5G",
                        "od_range": "4.500\" and above",
                        "wall_range": "0.188\" to 0.750\"",
                        "preheat_min": "100\u00b0F for WT \u2264 0.500\" / 150\u00b0F for WT > 0.500\"",
                        "interpass_max": "400\u00b0F",
                        "joint_design": "Single V-groove, 60\u00b0 included angle, 1/16\" land, 1/16\" to 3/32\" root opening",
                        "pwht": "Not required for X65 WT \u2264 0.750\"",
                        "current_polarity": "SMAW: DCEP / FCAW-G: DCEP",
                        "shielding_gas": "FCAW-G: 75% Ar / 25% CO\u2082 at 35\u201345 CFH",
                        "qualified_by": "PQR-CS-001A and PQR-CS-001B",
                        "note": "Root pass SMAW only. Fill and cap passes SMAW or FCAW-G. Post-weld hydrogen bake-out required for wall > 0.500\".",
                    },
                    {
                        "number": "WPS-CS-002 Rev. 2",
                        "process": "SMAW",
                        "base_metal": "API 5L X52 through X65",
                        "p_number": "P-1 Group 1",
                        "filler_root": "E7018-H4",
                        "filler_fill_cap": "E7018-H4",
                        "positions": "1G, 2G, 5G, 6G",
                        "od_range": "2.375\" and above",
                        "wall_range": "0.188\" to 0.500\"",
                        "preheat_min": "100\u00b0F",
                        "interpass_max": "400\u00b0F",
                        "joint_design": "Single V-groove, 60\u00b0 included angle, 1/16\" land, 1/16\" to 3/32\" root opening",
                        "pwht": "Not required",
                        "current_polarity": "DCEP",
                        "shielding_gas": "N/A",
                        "qualified_by": "PQR-CS-002",
                        "note": "All-position SMAW. Applies to branch connections and small-bore tie-in welds.",
                    },
                ],
                "welders": [
                    {
                        "name": "M. Torres",
                        "stamp": "W-042",
                        "wqr": "WQR-2024-042",
                        "processes": ["SMAW", "FCAW-G"],
                        "positions": ["1G", "2G", "5G", "6G"],
                        "base_metal": "API 5L up to X70 / ASTM A105N",
                        "od_min": "2.375\"",
                        "wall_range": "0.188\" to 0.750\"",
                        "expiry": "2026-08-15",
                        "continuity": "Active \u2014 last welded 03/10/2026",
                        "pqr_basis": "PQR-CS-001A (SMAW 5G, 12\" \u00d7 0.375\" X65)",
                    },
                    {
                        "name": "D. Kimura",
                        "stamp": "W-019",
                        "wqr": "WQR-2024-019",
                        "processes": ["SMAW", "FCAW-G"],
                        "positions": ["1G", "2G", "5G"],
                        "base_metal": "API 5L up to X70 / ASTM A105N",
                        "od_min": "2.375\"",
                        "wall_range": "0.188\" to 0.500\"",
                        "expiry": "2026-11-03",
                        "continuity": "Active \u2014 last welded 03/12/2026",
                        "pqr_basis": "PQR-CS-001B (SMAW/FCAW 5G, 12\" \u00d7 0.375\" X65)",
                    },
                    {
                        "name": "R. Castillo",
                        "stamp": "W-031",
                        "wqr": "WQR-2024-031",
                        "processes": ["SMAW"],
                        "positions": ["1G", "2G", "5G", "6G"],
                        "base_metal": "API 5L up to X65",
                        "od_min": "2.375\"",
                        "wall_range": "0.188\" to 0.500\"",
                        "expiry": "2026-09-22",
                        "continuity": "Active \u2014 last welded 03/11/2026",
                        "pqr_basis": "PQR-CS-002 (SMAW 6G, 6\" \u00d7 0.280\" X65)",
                    },
                ],
                "pipe_mtrs": [
                    {
                        "cert_no": "MTR-P-6901",
                        "manufacturer": "Lone Star Pipe & Steel, Houston TX 77029",
                        "spec": "API 5L PSL2",
                        "grade": "X65",
                        "heat_no": "HT-P-2244",
                        "po_no": "PO-55102",
                        "job_no": "MCK-2026-001",
                        "sizes_covered": [
                            "12.750\" OD \u00d7 0.375\" WT \u2014 40 joints",
                            "8.625\" OD \u00d7 0.322\" WT \u2014 12 joints",
                        ],
                        "chemistry": [
                            ["Element", "C", "Mn", "P", "S", "Si", "Nb", "V", "Ti", "Ceq"],
                            ["Required", "\u22640.22", "\u22641.65", "\u22640.025", "\u22640.015", "\u22640.45", "\u22640.05", "\u22640.05", "\u22640.04", "\u22640.43"],
                            ["Actual", "0.14", "1.42", "0.012", "0.003", "0.28", "0.038", "0.044", "0.015", "0.38"],
                        ],
                        "mechanical": [
                            ["Property", "Requirement", "Actual"],
                            ["Yield Strength", "\u226565,300 psi (450 MPa)", "71,800 psi"],
                            ["Tensile Strength", "\u226577,500 psi (535 MPa)", "84,200 psi"],
                            ["Elongation", "\u226521%", "28%"],
                            ["CVN at -20\u00b0F", "\u226530 ft-lb avg", "52 ft-lb avg"],
                            ["HIC Test (CLR)", "\u226415%", "0% \u2014 PASS"],
                            ["SSC Test", "NACE TM0177 Method A \u2014 PASS", "No cracking at 72 hrs"],
                        ],
                        "certification": "We hereby certify that the pipe described herein was manufactured, tested, and inspected in accordance with API 5L PSL2 Grade X65. All chemical, mechanical, and supplementary test results conform to specification requirements including sour service (HIC/SSC) testing.",
                        "certified_by": "J. Whitmore, Quality Manager",
                        "cert_date": "2025-12-01",
                        "sour_note": "HIC and SSC tested per NACE TM0284 and TM0177. Confirmed suitable for sour service (H\u2082S) applications.",
                    },
                    {
                        "cert_no": "MTR-P-6902",
                        "manufacturer": "Lone Star Pipe & Steel, Houston TX 77029",
                        "spec": "API 5L PSL2",
                        "grade": "X65",
                        "heat_no": "HT-P-2245",
                        "po_no": "PO-55102",
                        "job_no": "MCK-2026-001",
                        "sizes_covered": [
                            "6.625\" OD \u00d7 0.280\" WT \u2014 18 joints",
                        ],
                        "chemistry": [
                            ["Element", "C", "Mn", "P", "S", "Si", "Nb", "V", "Ti", "Ceq"],
                            ["Required", "\u22640.22", "\u22641.65", "\u22640.025", "\u22640.015", "\u22640.45", "\u22640.05", "\u22640.05", "\u22640.04", "\u22640.43"],
                            ["Actual", "0.12", "1.38", "0.010", "0.002", "0.24", "0.041", "0.039", "0.012", "0.36"],
                        ],
                        "mechanical": [
                            ["Property", "Requirement", "Actual"],
                            ["Yield Strength", "\u226565,300 psi", "69,400 psi"],
                            ["Tensile Strength", "\u226577,500 psi", "82,100 psi"],
                            ["Elongation", "\u226521%", "30%"],
                            ["CVN at -20\u00b0F", "\u226530 ft-lb avg", "48 ft-lb avg"],
                            ["HIC Test (CLR)", "\u226415%", "0% \u2014 PASS"],
                            ["SSC Test", "NACE TM0177 Method A \u2014 PASS", "No cracking at 72 hrs"],
                        ],
                        "certification": "We hereby certify that the pipe described herein conforms to API 5L PSL2 Grade X65 including sour service supplementary requirements.",
                        "certified_by": "J. Whitmore, Quality Manager",
                        "cert_date": "2025-12-01",
                        "sour_note": "HIC and SSC tested. Confirmed suitable for sour service.",
                    },
                ],
                "filler_certs": [
                    {
                        "cert_no": "FC-7018-221",
                        "manufacturer": "Lincoln Electric Co., Cleveland OH 44117",
                        "classification": "AWS A5.1 / A5.1M E7018-H4",
                        "lot_no": "LT-7018-221",
                        "heat_no": "HT-F-0901",
                        "product": "Excalibur 7018 MR Low-Hydrogen Electrode",
                        "sizes": ["3/32\"", "1/8\"", "5/32\""],
                        "po_no": "PO-55214",
                        "job_no": "MCK-2026-001",
                        "storage_req": "Store at 250\u2013300\u00b0F in holding oven. Electrodes exposed to atmosphere > 4 hours shall be re-dried at 500\u2013700\u00b0F for 1 hour before use.",
                        "diffusible_hydrogen": "\u22644 mL/100g deposited weld metal (H4 designation confirmed)",
                        "chemistry": [
                            ["Element", "C", "Mn", "Si", "P", "S", "Ni", "Cr", "Mo", "V"],
                            ["Required", "\u22640.15", "\u22650.60", "\u2014", "\u22640.035", "\u22640.035", "\u2014", "\u2014", "\u2014", "\u2014"],
                            ["Actual", "0.06", "1.04", "0.42", "0.014", "0.008", "0.02", "0.03", "0.01", "0.01"],
                        ],
                        "mechanical": [
                            ["Property", "Requirement", "Actual"],
                            ["Tensile Strength", "\u226570 ksi (480 MPa)", "78 ksi"],
                            ["Yield Strength", "\u226558 ksi (400 MPa)", "66 ksi"],
                            ["Elongation", "\u226522%", "28%"],
                            ["CVN at -20\u00b0F", "\u226520 ft-lb", "44 ft-lb"],
                        ],
                        "certification": "Lincoln Electric certifies that the electrodes in Lot LT-7018-221 were manufactured and tested in accordance with AWS A5.1/A5.1M E7018-H4. All chemical and mechanical test results meet specification requirements.",
                        "certified_by": "P. Nguyen, QA Director",
                        "cert_date": "2025-10-28",
                    },
                    {
                        "cert_no": "FC-71T-088",
                        "manufacturer": "Lincoln Electric Co., Cleveland OH 44117",
                        "classification": "AWS A5.20 / A5.20M E71T-1M-H8",
                        "lot_no": "LT-71T-088",
                        "heat_no": "HT-F-1102",
                        "product": "Innershield NR-232 FCAW-G Wire",
                        "sizes": ["0.045\"", "0.052\""],
                        "po_no": "PO-55214",
                        "job_no": "MCK-2026-001",
                        "storage_req": "Store in original sealed packaging in dry conditions. Once opened, use within 30 days or reseal. Shielding gas: 75% Ar / 25% CO\u2082.",
                        "diffusible_hydrogen": "\u22648 mL/100g deposited weld metal (H8 designation confirmed)",
                        "chemistry": [
                            ["Element", "C", "Mn", "Si", "P", "S", "Ni", "Cr", "Mo"],
                            ["Required", "\u22640.18", "\u22651.20", "\u22650.50", "\u22640.030", "\u22640.030", "\u2014", "\u2014", "\u2014"],
                            ["Actual", "0.06", "1.48", "0.62", "0.011", "0.006", "0.02", "0.02", "0.01"],
                        ],
                        "mechanical": [
                            ["Property", "Requirement", "Actual"],
                            ["Tensile Strength", "\u226570 ksi (480 MPa)", "76 ksi"],
                            ["Yield Strength", "\u226558 ksi (400 MPa)", "63 ksi"],
                            ["Elongation", "\u226522%", "26%"],
                            ["CVN at -20\u00b0F", "\u226520 ft-lb", "38 ft-lb"],
                        ],
                        "certification": "Lincoln Electric certifies that the wire in Lot LT-71T-088 conforms to AWS A5.20/A5.20M E71T-1M-H8. All test results meet specification requirements.",
                        "certified_by": "P. Nguyen, QA Director",
                        "cert_date": "2025-10-28",
                    },
                ],
                "travelers": [
                    {
                        "weld_id": "WLD-001",
                        "weld_map_no": "MCK-WM-2026-001 Sheet 3",
                        "description": "12\" Mainline Tie-In North End",
                        "pipe_heat": "HT-P-2244",
                        "pipe_cert": "MTR-P-6901",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_lot": "LT-71T-088",
                        "root_opening_measured": "5/64\"",
                        "hi_lo_measured": "3/32\"",
                        "bevel_angle_measured": "30\u00b0",
                        "land_measured": "1/16\"",
                        "cleanliness": "PASS \u2014 mill scale removed, no moisture",
                        "preheat_method": "Tempilstik",
                        "preheat_measured": "125\u00b0F",
                        "pass_log": [
                            {"pass": 1, "type": "Root", "process": "SMAW", "filler": "E7018-H4", "welder": "W-042", "interpass_before": "N/A"},
                            {"pass": 2, "type": "Hot Pass", "process": "SMAW", "filler": "E7018-H4", "welder": "W-042", "interpass_before": "285\u00b0F"},
                            {"pass": 3, "type": "Fill", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-042", "interpass_before": "310\u00b0F"},
                            {"pass": 4, "type": "Cap", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-042", "interpass_before": "325\u00b0F"},
                        ],
                        "interpass_high": "325\u00b0F",
                        "crown_height_measured": "3/32\"",
                        "undercut_measured": "None",
                        "visual_result": "ACC",
                        "nde_method": "RT",
                        "nde_procedure": "RT-PROC-004 Rev. 2",
                        "nde_tech": "B. Okafor RT Level II",
                        "nde_report": "RT-2026-044",
                        "nde_result": "ACC",
                        "final_disposition": "ACC",
                        "inspector": "T. Garza",
                        "inspector_initials": "T. GARZA",
                        "date": "03/14/2026",
                    },
                    {
                        "weld_id": "WLD-002",
                        "weld_map_no": "MCK-WM-2026-001 Sheet 3",
                        "pipe_heat": "HT-P-2244",
                        "pipe_cert": "MTR-P-6901",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_lot": "LT-71T-088",
                        "pass_log": [
                            {"pass": 1, "type": "Root", "process": "SMAW", "filler": "E7018-H4", "welder": "W-019", "interpass_before": "N/A"},
                            {"pass": 2, "type": "Hot Pass", "process": "SMAW", "filler": "E7018-H4", "welder": "W-019", "interpass_before": "278\u00b0F"},
                            {"pass": 3, "type": "Fill", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-019", "interpass_before": "295\u00b0F"},
                            {"pass": 4, "type": "Cap", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-019", "interpass_before": "310\u00b0F"},
                        ],
                        "interpass_high": "310\u00b0F",
                        "crown_height_measured": "3/32\"",
                        "undercut_measured": "None",
                        "visual_result": "ACC",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-045",
                        "nde_result": "ACC",
                        "final_disposition": "ACC",
                    },
                    {
                        "weld_id": "WLD-003",
                        "weld_map_no": "MCK-WM-2026-001 Sheet 4",
                        "pipe_heat": "HT-P-2244",
                        "pipe_cert": "MTR-P-6901",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_lot": "LT-7018-221",
                        "pass_log": [
                            {"pass": 1, "type": "Root", "process": "SMAW", "filler": "E7018-H4", "welder": "W-042", "interpass_before": "N/A"},
                            {"pass": 2, "type": "Fill", "process": "SMAW", "filler": "E7018-H4", "welder": "W-042", "interpass_before": "262\u00b0F"},
                            {"pass": 3, "type": "Cap", "process": "SMAW", "filler": "E7018-H4", "welder": "W-042", "interpass_before": "298\u00b0F"},
                        ],
                        "interpass_high": "298\u00b0F",
                        "crown_height_measured": "1/16\"",
                        "undercut_measured": "None",
                        "visual_result": "ACC",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-046",
                        "nde_result": "ACC",
                        "final_disposition": "ACC",
                    },
                    {
                        "weld_id": "WLD-004",
                        "weld_map_no": "MCK-WM-2026-001 Sheet 5",
                        "pipe_heat": "HT-P-2245",
                        "pipe_cert": "MTR-P-6902",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_lot": "LT-7018-221",
                        "pass_log": [
                            {"pass": 1, "type": "Root", "process": "SMAW", "filler": "E7018-H4", "welder": "W-031", "interpass_before": "N/A"},
                            {"pass": 2, "type": "Fill", "process": "SMAW", "filler": "E7018-H4", "welder": "W-031", "interpass_before": "248\u00b0F"},
                            {"pass": 3, "type": "Cap", "process": "SMAW", "filler": "E7018-H4", "welder": "W-031", "interpass_before": "285\u00b0F"},
                        ],
                        "interpass_high": "285\u00b0F",
                        "crown_height_measured": "1/16\"",
                        "undercut_measured": "None",
                        "visual_result": "ACC",
                        "nde_method": "UT",
                        "nde_report": "UT-2026-019",
                        "nde_result": "ACC",
                        "final_disposition": "ACC",
                    },
                    {
                        "weld_id": "WLD-005",
                        "weld_map_no": "MCK-WM-2026-001 Sheet 3",
                        "pipe_heat": "HT-P-2244",
                        "pipe_cert": "MTR-P-6901",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_lot": "LT-71T-088",
                        "pass_log": [
                            {"pass": 1, "type": "Root", "process": "SMAW", "filler": "E7018-H4", "welder": "W-019", "interpass_before": "N/A"},
                            {"pass": 2, "type": "Hot Pass", "process": "SMAW", "filler": "E7018-H4", "welder": "W-019", "interpass_before": "272\u00b0F"},
                            {"pass": 3, "type": "Fill", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-019", "interpass_before": "304\u00b0F"},
                            {"pass": 4, "type": "Cap", "process": "FCAW-G", "filler": "E71T-1M-H8", "welder": "W-019", "interpass_before": "318\u00b0F"},
                        ],
                        "interpass_high": "318\u00b0F",
                        "crown_height_measured": "3/32\"",
                        "undercut_measured": "None",
                        "visual_result": "ACC",
                        "nde_method": "RT",
                        "nde_report": "RT-2026-047",
                        "nde_result": "ACC",
                        "final_disposition": "ACC",
                    },
                ],
            },
            "step_fields": {
                "wps_verification": [
                    {"key": "wps_number", "label": "Applicable WPS No.", "section": "identification", "hint": "WPS-XX-XXX Rev. X \u2014 match OD, WT, grade, process, and position", "tooltip": "Check OD range, wall range, base metal grade, process, and position against both WPS documents."},
                    {"key": "welding_process", "label": "Welding Process(es)", "section": "identification", "hint": "e.g. SMAW/FCAW \u2014 as listed on the WPS for this joint", "tooltip": "Record the process(es) on the WPS. Multi-process joints list both."},
                    {"key": "positions_covered", "label": "Positions Covered by WPS", "section": "coverage", "hint": "List all positions on this WPS e.g. 1G, 2G, 5G", "tooltip": "Copy the positions list from the WPS. Confirm 5G is included for this joint."},
                    {"key": "od_range", "label": "OD Range Covered", "section": "coverage", "hint": "e.g. 4.500\" and above \u2014 from WPS essential variables", "tooltip": "The WPS must cover the OD of the pipe being welded. Find this in the essential variables section."},
                    {"key": "wall_range", "label": "Wall Thickness Range", "section": "coverage", "hint": "e.g. 0.188\" to 0.750\" \u2014 from WPS essential variables", "tooltip": "The actual wall thickness must fall within this range."},
                    {"key": "base_metal_covered", "label": "Base Metal Covered", "section": "coverage", "hint": "e.g. API 5L X52 through X70 \u2014 from WPS base metal section", "tooltip": "The pipe grade must fall within the base metal range qualified by the WPS."},
                    {"key": "preheat_min", "label": "Min. Preheat (\u00b0F) \u2014 this WT", "section": "parameters", "hint": "Numeric \u2014 from WPS preheat table for WT \u2264 0.500\"", "tooltip": "The WPS has a tiered preheat requirement by wall thickness. Use the row that covers 0.375\"."},
                    {"key": "interpass_max", "label": "Max. Interpass Temp (\u00b0F)", "section": "parameters", "hint": "Numeric \u2014 from WPS interpass temperature limit", "tooltip": "The ceiling temperature between passes. A required entry on every joint traveler."},
                    {"key": "filler_root", "label": "Filler Metal \u2014 Root Pass", "section": "parameters", "hint": "AWS class \u2014 e.g. E7018-H4", "tooltip": "Copy the root pass filler classification from the WPS filler metal section."},
                    {"key": "filler_fill", "label": "Filler Metal \u2014 Fill/Cap", "section": "parameters", "hint": "AWS class \u2014 e.g. E71T-1M-H8 or same as root", "tooltip": "May differ from the root pass. Copy from the WPS for fill and cap passes."},
                    {"key": "pwht_required", "label": "PWHT Required?", "section": "parameters", "hint": "Yes or No \u2014 from WPS PWHT section for this material and WT", "tooltip": "Check the WPS PWHT section. For X65 at 0.375\" wall the answer is stated explicitly."},
                ],
                "material_traceability": [
                    {"key": "pipe_spec", "label": "Pipe Spec / Grade", "section": "pipe", "hint": "e.g. API 5L X65 \u2014 from the pipe MTR", "tooltip": "Copy the specification and grade from the pipe Mill Test Report header."},
                    {"key": "pipe_heat", "label": "Pipe Heat No.", "section": "pipe", "hint": "Format: HT-X-XXXX \u2014 from the pipe MTR heat number field", "tooltip": "The heat number on the MTR must match the heat marked on the pipe. Find it in the MTR header block."},
                    {"key": "pipe_cert", "label": "Pipe MTR Cert No.", "section": "pipe", "hint": "Format: MTR-X-XXXX \u2014 the document number of the pipe MTR", "tooltip": "This is the MTR document number, not the heat number. Both are required on the traveler."},
                    {"key": "pipe_od_confirmed", "label": "Pipe OD", "section": "pipe", "hint": "e.g. 12.750\" \u2014 verify against MTR sizes covered", "tooltip": "Confirm the OD you are welding is in the sizes covered section of the MTR on file."},
                    {"key": "sour_service_confirmed", "label": "Sour Service Testing", "section": "pipe", "hint": "PASS or FAIL \u2014 from MTR HIC and SSC test results", "tooltip": "This is a sour service application. The MTR must confirm HIC and SSC testing per NACE TM0284 and TM0177."},
                    {"key": "filler_root_class", "label": "Root Filler Classification", "section": "filler", "hint": "AWS class \u2014 e.g. E7018-H4 \u2014 from filler cert", "tooltip": "Copy the AWS classification from the filler metal certificate. Must match the WPS."},
                    {"key": "filler_root_lot", "label": "Root Filler Lot No.", "section": "filler", "hint": "Format: LT-XXXX-XXX \u2014 from the filler metal certificate", "tooltip": "Lot traceability is required for filler metals. Find the lot number on the certificate header."},
                    {"key": "filler_fill_class", "label": "Fill/Cap Filler Classification", "section": "filler", "hint": "AWS class \u2014 e.g. E71T-1M-H8 \u2014 from filler cert", "tooltip": "Copy from the fill/cap filler cert. For SMAW-only joints this will match the root."},
                    {"key": "filler_fill_lot", "label": "Fill/Cap Filler Lot No.", "section": "filler", "hint": "Format: LT-XXXX-XXX \u2014 from the fill filler certificate", "tooltip": "If root and fill use the same electrode, the lot number may be the same."},
                    {"key": "welder_stamp", "label": "Welder Stamp", "section": "welder", "hint": "Format: W-XXX \u2014 from the WQR on file for this welder", "tooltip": "The unique welder stamp. Must appear on the WQR and will be marked on the pipe at the joint."},
                    {"key": "wqr_number", "label": "WQR Number", "section": "welder", "hint": "Format: WQR-YYYY-XXX \u2014 from the welder qualification record", "tooltip": "The document number of the qualification record that supports this welder for this WPS and position."},
                    {"key": "welder_continuity", "label": "Welder Continuity Status", "section": "welder", "hint": "Active or Lapsed \u2014 from the WQR continuity field", "tooltip": "A welder who has not used this process in 6 months is lapsed and cannot weld without requalification."},
                ],
                "pre_weld_fitup": [
                    {"key": "root_opening", "label": "Root Opening", "section": "fitup", "hint": "Fraction in inches \u2014 measured value e.g. 5/64\"", "tooltip": "Acceptable range per WPS: 1/16\" to 3/32\" (4/64\" to 6/64\"). Measure with a feeler gauge or root opening gauge."},
                    {"key": "hi_lo", "label": "Hi-Lo (Internal Misalignment)", "section": "fitup", "hint": "Fraction in inches \u2014 measured with hi-lo gauge", "tooltip": "Maximum allowable is 1/8\" or 10% of wall thickness, whichever is less. 10% of 0.375\" = 0.0375\" \u2248 3/80\"."},
                    {"key": "bevel_angle", "label": "Bevel Angle (per side)", "section": "fitup", "hint": "Degrees \u2014 e.g. 30\u00b0 measured with a bevel protractor", "tooltip": "WPS requires 30\u00b0 \u00b1 2.5\u00b0 per side. Total included angle = 60\u00b0."},
                    {"key": "land", "label": "Land (Root Face)", "section": "fitup", "hint": "Fraction in inches \u2014 e.g. 1/16\"", "tooltip": "WPS requires 1/16\" \u00b1 1/32\". Measure with a ruler or vernier caliper at multiple points around the joint."},
                    {"key": "fitup_result", "label": "Fit-Up Result", "section": "fitup", "hint": "ACC or REJ \u2014 based on all four measurements above", "tooltip": "All four measurements must be within tolerance. If any is outside range, result is REJ and fit-up must be corrected."},
                    {"key": "cleanliness", "label": "Joint Cleanliness", "section": "preweld", "hint": "PASS or FAIL \u2014 check bevel and 1\" each side for scale, moisture, oil", "tooltip": "Visually inspect bevel faces and 1\" adjacent pipe. Any mill scale, rust, moisture, paint, or oil is FAIL."},
                    {"key": "preheat_method", "label": "Preheat Method", "section": "preweld", "hint": "e.g. Tempilstik or Infrared \u2014 measurement device used", "tooltip": "Acceptable methods are temperature-indicating sticks (Tempilstik) or calibrated infrared thermometer. Record which was used."},
                    {"key": "preheat_measured", "label": "Preheat Temp Measured (\u00b0F)", "section": "preweld", "hint": "Numeric \u2014 actual temperature measured before root pass", "tooltip": "Must meet or exceed the WPS minimum. Measure within 1\" of the joint on both sides. Record the actual value, not the minimum."},
                    {"key": "preheat_result", "label": "Preheat Result", "section": "preweld", "hint": "ACC or REJ \u2014 measured temp vs WPS minimum requirement", "tooltip": "ACC if measured preheat \u2265 WPS minimum. REJ if below minimum \u2014 welding cannot begin until preheat requirement is met."},
                ],
                "in_process_log": [
                    {"key": "welder_stamp", "label": "Welder\nStamp", "hint": "W-XXX"},
                    {"key": "passes", "label": "Total\nPasses", "hint": "Whole number"},
                    {"key": "interpass_high", "label": "Interpass\nHigh (\u00b0F)", "hint": "e.g. 325"},
                    {"key": "filler_root", "label": "Root Pass\nFiller", "hint": "AWS class"},
                    {"key": "filler_fill", "label": "Fill/Cap\nFiller", "hint": "AWS class"},
                    {"key": "in_process_ok", "label": "In-Process\nResult", "hint": "ACC or REJ"},
                ],
                "final_inspection": [
                    {"key": "crown_height", "label": "Crown\nHeight", "hint": "e.g. 3/32\""},
                    {"key": "undercut", "label": "Undercut", "hint": "None or depth"},
                    {"key": "visual_result", "label": "Visual\nResult", "hint": "ACC or REJ"},
                    {"key": "nde_method", "label": "NDE\nMethod", "hint": "RT or UT"},
                    {"key": "nde_report", "label": "NDE Report\nNo.", "hint": "RT-YYYY-XXX"},
                    {"key": "nde_result", "label": "NDE\nResult", "hint": "ACC or REJ"},
                    {"key": "disposition", "label": "Final\nDisposition", "hint": "ACC or REJ"},
                ],
            },
            "answers": {
                "wps_verification": {
                    "WLD-001": {
                        "wps_number": "WPS-CS-001 Rev. 4",
                        "welding_process": "SMAW/FCAW",
                        "positions_covered": "1G, 2G, 5G",
                        "od_range": "4.500\" and above",
                        "wall_range": "0.188\" to 0.750\"",
                        "base_metal_covered": "API 5L X52 through X70",
                        "preheat_min": "100",
                        "interpass_max": "400",
                        "filler_root": "E7018-H4",
                        "filler_fill": "E71T-1M-H8",
                        "pwht_required": "No",
                    },
                },
                "material_traceability": {
                    "WLD-001": {
                        "pipe_spec": "API 5L X65",
                        "pipe_heat": "HT-P-2244",
                        "pipe_cert": "MTR-P-6901",
                        "pipe_od_confirmed": "12.750\"",
                        "sour_service_confirmed": "PASS",
                        "filler_root_class": "E7018-H4",
                        "filler_root_lot": "LT-7018-221",
                        "filler_fill_class": "E71T-1M-H8",
                        "filler_fill_lot": "LT-71T-088",
                        "welder_stamp": "W-042",
                        "wqr_number": "WQR-2024-042",
                        "welder_continuity": "Active",
                    },
                },
                "pre_weld_fitup": {
                    "WLD-001": {
                        "root_opening": "5/64\"",
                        "hi_lo": "3/32\"",
                        "bevel_angle": "30\u00b0",
                        "land": "1/16\"",
                        "fitup_result": "ACC",
                        "cleanliness": "PASS",
                        "preheat_method": "Tempilstik",
                        "preheat_measured": "125",
                        "preheat_result": "ACC",
                    },
                },
                "in_process_log": {
                    "WLD-001": {"welder_stamp": "W-042", "passes": "4", "interpass_high": "325", "filler_root": "E7018-H4", "filler_fill": "E71T-1M-H8", "in_process_ok": "ACC"},
                    "WLD-002": {"welder_stamp": "W-019", "passes": "4", "interpass_high": "310", "filler_root": "E7018-H4", "filler_fill": "E71T-1M-H8", "in_process_ok": "ACC"},
                    "WLD-003": {"welder_stamp": "W-042", "passes": "3", "interpass_high": "298", "filler_root": "E7018-H4", "filler_fill": "E7018-H4", "in_process_ok": "ACC"},
                    "WLD-004": {"welder_stamp": "W-031", "passes": "3", "interpass_high": "285", "filler_root": "E7018-H4", "filler_fill": "E7018-H4", "in_process_ok": "ACC"},
                    "WLD-005": {"welder_stamp": "W-019", "passes": "4", "interpass_high": "318", "filler_root": "E7018-H4", "filler_fill": "E71T-1M-H8", "in_process_ok": "ACC"},
                },
                "final_inspection": {
                    "WLD-001": {"crown_height": "3/32\"", "undercut": "None", "visual_result": "ACC", "nde_method": "RT", "nde_report": "RT-2026-044", "nde_result": "ACC", "disposition": "ACC"},
                    "WLD-002": {"crown_height": "3/32\"", "undercut": "None", "visual_result": "ACC", "nde_method": "RT", "nde_report": "RT-2026-045", "nde_result": "ACC", "disposition": "ACC"},
                    "WLD-003": {"crown_height": "1/16\"", "undercut": "None", "visual_result": "ACC", "nde_method": "RT", "nde_report": "RT-2026-046", "nde_result": "ACC", "disposition": "ACC"},
                    "WLD-004": {"crown_height": "1/16\"", "undercut": "None", "visual_result": "ACC", "nde_method": "UT", "nde_report": "UT-2026-019", "nde_result": "ACC", "disposition": "ACC"},
                    "WLD-005": {"crown_height": "3/32\"", "undercut": "None", "visual_result": "ACC", "nde_method": "RT", "nde_report": "RT-2026-047", "nde_result": "ACC", "disposition": "ACC"},
                },
            },
        }

        exercise, ex_created = InteractiveExercise.objects.get_or_create(
            lesson=lesson_15,
            defaults={
                'exercise_type': 'weld_log',
                'passing_score': 80,
                'version': '1.0',
                'config': exercise_config,
            },
        )
        if not ex_created and exercise.config != exercise_config:
            exercise.config = exercise_config
            exercise.save()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # SUMMARY
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lesson_count = Lesson.objects.filter(module=mod3).count()
        exercise_count = InteractiveExercise.objects.filter(lesson__module=mod3).count()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('\u2501\u2501 Summary \u2501\u2501'))
        self.stdout.write(
            f'Module 3: {"created" if mod3_created else "found"} \u2014 '
            f'{mod3.title} [GATED]'
        )
        self.stdout.write(f'Lessons: {lesson_count} (orders 10\u201315)')
        self.stdout.write(
            f'Exercise: weld_log {"created" if ex_created else "found"} \u2014 '
            f'passing score {exercise.passing_score}%'
        )
        self.stdout.write('')
        self.stdout.write(
            'Note: weld_log exercise type requires a separate bundle build. '
            'The exercise config is stored in the database. Build the React '
            'component at static/exercises/bundle.js to handle '
            'window.EXERCISE_TYPE === \'weld_log\'.'
        )
