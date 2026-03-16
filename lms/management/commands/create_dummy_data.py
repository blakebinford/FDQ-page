from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from applications.models import Application
from lms.models import (
    Tier, Module, Lesson, Quiz, Question, InteractiveExercise,
)


class Command(BaseCommand):
    help = 'Create dummy data for local development and testing.'

    def handle(self, *args, **options):
        # ── TIER 1 ──
        tier, tier_created = Tier.objects.get_or_create(
            slug='practitioner',
            defaults={
                'name': 'Practitioner',
                'description': 'Foundational field quality for crew and inspectors.',
                'price_cents': 50000,
                'stripe_price_id': 'price_test_placeholder',
                'order': 1,
                'prerequisite': None,
                'is_active': True,
            },
        )
        self.stdout.write(f'Tier 1: {"created" if tier_created else "found"} — {tier.name}')

        # ── TIER 2 ──
        tier2, tier2_created = Tier.objects.get_or_create(
            slug='implementer',
            defaults={
                'name': 'Implementer',
                'description': 'Field quality deployment for QC professionals and operations leads.',
                'price_cents': 75000,
                'stripe_price_id': 'price_test_placeholder_t2',
                'order': 2,
                'prerequisite': tier,
                'is_active': True,
            },
        )
        if not tier2_created and tier2.prerequisite != tier:
            tier2.prerequisite = tier
            tier2.save()
        self.stdout.write(f'Tier 2: {"created" if tier2_created else "found"} — {tier2.name}')

        # ── TIER 3 ──
        tier3, tier3_created = Tier.objects.get_or_create(
            slug='director',
            defaults={
                'name': 'Director',
                'description': 'Quality program design and leadership for senior quality professionals.',
                'price_cents': 100000,
                'stripe_price_id': 'price_test_placeholder_t3',
                'order': 3,
                'prerequisite': tier2,
                'is_active': True,
            },
        )
        if not tier3_created and tier3.prerequisite != tier2:
            tier3.prerequisite = tier2
            tier3.save()
        self.stdout.write(f'Tier 3: {"created" if tier3_created else "found"} — {tier3.name}')

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # MODULE 1 — Bolted Flange Fundamentals (gated)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        mod1, _ = Module.objects.get_or_create(
            tier=tier, order=1,
            defaults={'title': 'Bolted Flange Fundamentals', 'gate_required': True},
        )
        if not mod1.gate_required:
            mod1.gate_required = True
            mod1.save()
        if mod1.title != 'Bolted Flange Fundamentals':
            mod1.title = 'Bolted Flange Fundamentals'
            mod1.save()

        # ── Lesson 1 ──
        Lesson.objects.get_or_create(
            module=mod1, order=1,
            defaults={
                'title': 'Reading a Company Specification',
                'content_type': 'reading',
                'estimated_minutes': 7,
                'body': (
                    '<p>A piping specification is the governing document for every bolted '
                    'flange connection on a project. Before you touch a wrench, you need to '
                    'know how to read one. Specs are organized into numbered sections — scope, '
                    'referenced standards, material requirements, gasket requirements, '
                    'lubrication, bolt tightening procedure, torque values, and inspection '
                    'documentation. Understanding the document hierarchy is critical: the '
                    'project specification supersedes the procedure, and the procedure '
                    'supersedes general workmanship standards. When a conflict exists between '
                    'documents, the spec wins.</p>'

                    '<p>The torque table is the section you will reference most often. It lists '
                    'target torque values by NPS (nominal pipe size) and pressure class. Each '
                    'row gives you the bolt size, quantity, snug torque, intermediate torque, '
                    'and final torque in foot-pounds. You must match the NPS and class of your '
                    'joint exactly — do not interpolate between rows or guess. The table also '
                    'specifies the minimum number of passes and the maximum allowable torque '
                    '(typically 120% of final). Exceeding maximum torque means bolt replacement.</p>'

                    '<p>Acceptance criteria define what makes a joint ACC (Accepted) or REJ '
                    '(Rejected). In most specs, §10.3 or its equivalent states: a joint is ACC '
                    'when achieved torque equals the final torque value ±5%, no bolt advanced '
                    'during the final re-check pass, and no visible leakage or gasket extrusion '
                    'is present. Anything outside these conditions is REJ and requires an NCR.</p>'

                    '<p>Finally, the spec dictates the inspector identification format. On '
                    'MEP-QC-FORM-044A, the inspector must record their initials as first '
                    'initial, period, space, full surname — all in capital letters (e.g., '
                    '<strong>J. SMITH</strong>). Abbreviated or lowercase entries are '
                    'non-compliant. This format links the record to the inspector\'s '
                    'qualification file for audit traceability.</p>'
                ),
            },
        )

        # ── Lesson 2 ──
        Lesson.objects.get_or_create(
            module=mod1, order=2,
            defaults={
                'title': 'MTR Traceability and What to Look For',
                'content_type': 'reading',
                'estimated_minutes': 8,
                'body': (
                    '<p>A Mill Test Report (MTR) is a certified document from the material '
                    'manufacturer that proves the bolts, nuts, flanges, or gaskets you are '
                    'installing were manufactured and tested to the specification printed on '
                    'your engineering drawings. MTRs are not optional paperwork — they are the '
                    'legal proof of material compliance. Every piece of pressure-retaining '
                    'material on your job must be traceable to an MTR before it goes into the '
                    'system.</p>'

                    '<p>Two numbers on the MTR matter most: the <strong>heat number</strong> '
                    'and the <strong>cert number</strong>. The heat number identifies the '
                    'specific melt of steel — every bolt from that melt shares the same '
                    'chemistry and mechanical properties. The cert number is the document ID '
                    'of the MTR itself (e.g., MTR-8801). You record both on your torque form. '
                    'A common mistake is confusing the two: the heat number tells you '
                    '<em>what metal</em> you have; the cert number tells you <em>which '
                    'document</em> proves it.</p>'

                    '<p>Watch for the two-heat trap. A single supplier may ship flanges from '
                    'two different heats — Heat A covering 4" and 6" sizes, Heat B covering '
                    '1.5" and 3" sizes. Each heat has its own MTR with its own cert number. '
                    'If you record Heat A\'s cert for a 3" flange, your traceability is wrong '
                    'even though the material is physically correct. Always check the "Sizes '
                    'Covered" section of the MTR to confirm which heat applies to your '
                    'joint\'s NPS.</p>'

                    '<p>For chemistry and mechanical properties, focus on the "Actual" row '
                    'versus the "Required" row. Every actual value must fall within the '
                    'required range — if any value is outside specification, the MTR should '
                    'show a rejection. For sour service (H₂S environments), ASTM A193 B7 '
                    'bolting has an additional hardness requirement: ≤35 HRC per NACE '
                    'MR0175. The MTR must explicitly confirm this. If the hardness row is '
                    'missing or exceeds 35 HRC, the bolts cannot be used in sour service '
                    'regardless of other properties.</p>'
                ),
            },
        )

        # ── Lesson 3 ──
        Lesson.objects.get_or_create(
            module=mod1, order=3,
            defaults={
                'title': 'Gasket Selection, Lot Numbers, and Handling',
                'content_type': 'reading',
                'estimated_minutes': 5,
                'body': (
                    '<p>For ASME B16.5 raised-face flanged connections in gas, sour gas, or '
                    'hydrocarbon service, the standard gasket is a spiral wound gasket (SWG) '
                    'conforming to ASME B16.20. The winding material for sour service is '
                    '316 stainless steel with flexible graphite filler (316SS/FG). The gasket '
                    'must include an outer centering ring and an inner retaining ring. No '
                    'substitutions are permitted without engineering approval.</p>'

                    '<p>Lot traceability is as important for gaskets as heat traceability is '
                    'for bolts. Each gasket lot is assigned a manufacturer\'s lot number '
                    '(e.g., GT-2241) printed on the packaging label and the certificate of '
                    'conformance. You record this lot number on MEP-QC-FORM-044A for every '
                    'joint. Do not estimate or copy lot numbers from adjacent joints — verify '
                    'each one from the packaging or cert. Spiral wound gaskets are '
                    '<strong>single-use items</strong>. A gasket removed from a previously '
                    'assembled joint must never be reinstalled, regardless of how good it '
                    'looks.</p>'

                    '<p>Before installing any gasket, perform a visual inspection. Reject '
                    'gaskets with crushed or separated windings, missing centering or '
                    'retaining rings, scoring on seating surfaces, or visible corrosion. '
                    'Mark rejected gaskets clearly and quarantine them so they cannot be '
                    'accidentally installed. Confirm that the gasket inner diameter does not '
                    'restrict the pipe bore — an oversized-ID gasket protruding into the '
                    'flow stream is a nonconformance.</p>'
                ),
            },
        )

        # ── Lesson 4 ──
        Lesson.objects.get_or_create(
            module=mod1, order=4,
            defaults={
                'title': 'Torque Procedure Basics',
                'content_type': 'reading',
                'estimated_minutes': 8,
                'body': (
                    '<p>Torque is a means to an end — the end is bolt load. It is the '
                    'clamping force on the gasket that creates the seal, not the torque value '
                    'itself. The relationship between applied torque and resulting bolt load '
                    'depends on the nut factor (K-factor), which accounts for friction in the '
                    'threads and under the nut face. For lubricated ASTM A193 B7 / A194 2H '
                    'assemblies using Molykote G-1000, the K-factor is 0.16. This is the '
                    'basis for every torque value in the specification.</p>'

                    '<p>Lubrication is not optional. Applying the same torque value to a dry '
                    'bolt produces 30–40% less bolt load than applying it to a properly '
                    'lubricated bolt. This means a "passing" torque reading on a dry bolt '
                    'is actually a failing joint — the gasket is under-compressed and will '
                    'leak. Always apply lubricant to the full thread length and the nut '
                    'bearing face before assembly. The specification prohibits anti-seize '
                    'compounds containing lead, zinc, or cadmium.</p>'

                    '<p>The cross (star) pattern is required for all joints. Starting at the '
                    '12 o\'clock bolt, you tighten the diametrically opposite bolt, then '
                    'rotate 90° and repeat. This sequence distributes load evenly across the '
                    'gasket and prevents flange cocking. Multi-pass torquing builds load '
                    'incrementally: Pass 1 (snug) seats the gasket at ~35% of final torque, '
                    'Pass 2 (intermediate) brings it to ~70%, and Pass 3 (final) achieves '
                    '100%. For NPS 1.5" and smaller in Class 600, a two-pass procedure is '
                    'permitted: Pass 1 at 50%, Pass 2 at 100%.</p>'

                    '<p>"Achieved torque" is the value recorded at the completion of the '
                    'final pass on the last bolt in the cross sequence. If any bolt advances '
                    '(moves) when you apply the final torque value, you must repeat the '
                    'entire final pass in cross pattern until no bolt advances. The highest '
                    'stable torque value applied uniformly across all bolts is the achieved '
                    'torque. This is the number that goes on the form — not the target, but '
                    'the actual value you verified in the field.</p>'
                ),
            },
        )

        # ── Lesson 5 — Interactive Exercise ──
        lesson_5, l5_created = Lesson.objects.get_or_create(
            module=mod1, order=5,
            defaults={
                'title': 'Practical Exercise: Bolted Flange Torque Log',
                'content_type': 'interactive',
                'estimated_minutes': 30,
                'body': '',
            },
        )
        if not l5_created and lesson_5.content_type != 'interactive':
            lesson_5.content_type = 'interactive'
            lesson_5.title = 'Practical Exercise: Bolted Flange Torque Log'
            lesson_5.estimated_minutes = 30
            lesson_5.body = ''
            lesson_5.save()

        # ── InteractiveExercise for Lesson 5 ──
        exercise_config = {
            "exercise_type": "torque_form",
            "title": "Bolted Flange Torque Log",
            "subtitle": "FDQ Tier 1 \u00b7 Module 1 Gate Exercise",
            "project": "Mustang Creek Compressor Station",
            "system": "Discharge Piping \u2014 Train A",
            "spec": "Q-SPEC-2200 Rev. 3",
            "procedure": "ASME B16.5 Class 600 / TQ-44A",
            "service": "Natural Gas \u2014 Sour Service",
            "total_steps": 2,
            "steps": [
                {
                    "id": "pre_assembly_form",
                    "label": "Step 1 of 2 \u2014 Pre-Assembly Form",
                    "description": "Fill MEP-QC-FORM-044A from spec, MTRs & drawing",
                },
                {
                    "id": "torque_log",
                    "label": "Step 2 of 2 \u2014 Torque Log",
                    "description": "Record achieved torque values after assembly",
                },
            ],
            "scenario": {
                "gasketLot": "GT-2241",
                "inspector": "J. Reed",
                "joints": [
                    {"id": "FLG-001", "location": "Suction Nozzle N1", "size": "6\"", "target": 185, "pattern": "Cross", "passes": 3},
                    {"id": "FLG-002", "location": "Discharge Nozzle N2", "size": "6\"", "target": 185, "pattern": "Cross", "passes": 3},
                    {"id": "FLG-003", "location": "Recycle Line Tie-In", "size": "4\"", "target": 120, "pattern": "Cross", "passes": 3},
                    {"id": "FLG-004", "location": "PSV-101 Inlet", "size": "3\"", "target": 120, "pattern": "Cross", "passes": 3},
                    {"id": "FLG-005", "location": "Drain Connection", "size": "1.5\"", "target": 65, "pattern": "Cross", "passes": 2},
                ],
            },
            "reference_docs": {
                "iso_drawing": {},
                "spec": {},
                "mtrs": {},
                "cal_cert": {},
                "joint_forms": {},
            },
        }

        exercise, ex_created = InteractiveExercise.objects.get_or_create(
            lesson=lesson_5,
            defaults={
                'exercise_type': 'torque_form',
                'passing_score': 80,
                'version': '1.0',
                'config': exercise_config,
            },
        )
        if not ex_created:
            exercise.exercise_type = 'torque_form'
            exercise.passing_score = 80
            exercise.version = '1.0'
            exercise.config = exercise_config
            exercise.save()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # MODULE 2 — Inspection and Documentation (not gated)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        mod2, _ = Module.objects.get_or_create(
            tier=tier, order=2,
            defaults={'title': 'Inspection and Documentation', 'gate_required': False},
        )

        # ── Lesson 6 — Weld Inspection Basics ──
        Lesson.objects.get_or_create(
            module=mod2, order=6,
            defaults={
                'title': 'Weld Inspection Basics',
                'content_type': 'reading',
                'estimated_minutes': 10,
                'body': (
                    '<p>Visual weld inspection is the most frequently performed '
                    'and most cost-effective NDE method on any construction site. '
                    'A trained inspector can catch undercut, porosity, '
                    'incomplete fusion, and incorrect weld profiles before '
                    'the joint moves to the next fabrication step.</p>'
                    '<p>Every visual inspection starts with three questions: Is '
                    'the correct WPS posted and followed? Does the welder hold a '
                    'valid qualification for this joint configuration? Are the '
                    'consumables (rod, wire, gas) matched to the procedure? If '
                    'any answer is no, the weld should not proceed.</p>'
                    '<p>During and after welding, check root pass penetration, '
                    'interpass temperature, final weld size against the minimum '
                    'fillet or groove dimension, and surface condition. Record '
                    'findings on the weld inspection report and disposition any '
                    'defects through the NCR process.</p>'
                ),
            },
        )

        # ── Lesson 7 — Coating and Surface Prep ──
        Lesson.objects.get_or_create(
            module=mod2, order=7,
            defaults={
                'title': 'Coating and Surface Prep',
                'content_type': 'reading',
                'estimated_minutes': 8,
                'body': (
                    '<p>Protective coatings fail for one reason more than any '
                    'other: inadequate surface preparation. Whether the '
                    'specification calls for SSPC-SP 6 (commercial blast), '
                    'SP 10 (near-white), or SP 5 (white metal), the standard '
                    'must be met and verified before the first coat is '
                    'applied.</p>'
                    '<p>Before blasting, confirm that the ambient temperature is '
                    'at least 5 \u00b0F above the dew point, relative humidity is '
                    'within the coating manufacturer\'s limits, and compressed '
                    'air is oil- and moisture-free. After blasting, measure the '
                    'surface profile with replica tape or a digital gauge and '
                    'compare it to the coating data sheet range.</p>'
                    '<p>Coating application requires wet-film thickness checks '
                    'during application and dry-film thickness verification after '
                    'cure. Document each coat \u2014 primer, intermediate, topcoat \u2014 '
                    'with batch numbers, mil readings, and environmental '
                    'conditions at time of application.</p>'
                ),
            },
        )

        # ── Lesson 8 — NCR Lifecycle ──
        Lesson.objects.get_or_create(
            module=mod2, order=8,
            defaults={
                'title': 'NCR Lifecycle',
                'content_type': 'reading',
                'estimated_minutes': 7,
                'body': (
                    '<p>A nonconformance report (NCR) documents any condition '
                    'where work, material, or documentation does not meet the '
                    'specified requirement. NCRs are not punitive \u2014 they are the '
                    'formal mechanism for identifying, evaluating, and resolving '
                    'quality deviations.</p>'
                    '<p>The NCR lifecycle has five stages: initiation (describing '
                    'the nonconformance and affected scope), evaluation '
                    '(engineering review of the deviation), disposition (accept '
                    'as-is, repair, rework, or reject/replace), corrective action '
                    '(implementing the disposition), and closeout (verifying the '
                    'corrective action and archiving the record).</p>'
                    '<p>Timely NCR closure is critical. Open NCRs block turnover '
                    'packages and signal unresolved quality risk. Track NCR '
                    'aging weekly and escalate any item open beyond the agreed '
                    'resolution window.</p>'
                ),
            },
        )

        # ── Lesson 9 — Turnover Documentation ──
        Lesson.objects.get_or_create(
            module=mod2, order=9,
            defaults={
                'title': 'Turnover Documentation',
                'content_type': 'reading',
                'estimated_minutes': 6,
                'body': (
                    '<p>Turnover documentation is the final deliverable of the '
                    'quality program. It proves to the owner and regulator that '
                    'every component was installed, inspected, and tested in '
                    'accordance with the design and applicable codes.</p>'
                    '<p>A typical turnover package includes the ITP with all '
                    'sign-offs complete, material test reports (MTRs), weld maps '
                    'and NDE reports, pressure test records, coating inspection '
                    'reports, and a punch list showing all items cleared. Missing '
                    'or incomplete documents are the number-one cause of turnover '
                    'delays.</p>'
                    '<p>Start assembling packages early \u2014 do not wait until '
                    'mechanical completion. Assign a document controller to '
                    'track completion status by system, and conduct weekly '
                    'reviews to identify gaps while there is still time to '
                    'recover records from the field.</p>'
                ),
            },
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # QUIZ — covers both modules
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        quiz, _ = Quiz.objects.get_or_create(
            tier=tier,
            defaults={
                'title': 'FDQ Practitioner Assessment',
                'passing_score': 80,
            },
        )

        questions = [
            {
                'order': 1,
                'text': 'What is the primary goal of Field-Driven Quality?',
                'choice_a': 'Reduce the number of inspectors on site',
                'choice_b': 'Shift quality ownership to the crew performing the work',
                'choice_c': 'Eliminate all documentation requirements',
                'choice_d': 'Replace engineering review with field decisions',
                'correct_answer': 'b',
            },
            {
                'order': 2,
                'text': 'Which of the following is NOT part of a pre-task quality check?',
                'choice_a': 'Material traceability verification',
                'choice_b': 'Procedure revision confirmation',
                'choice_c': 'Final turnover package assembly',
                'choice_d': 'Tooling and calibration verification',
                'correct_answer': 'c',
            },
            {
                'order': 3,
                'text': 'An Inspection and Test Plan (ITP) primarily defines:',
                'choice_a': 'The project schedule and milestones',
                'choice_b': 'Each inspection point, acceptance criteria, and responsible parties',
                'choice_c': 'The total budget for quality activities',
                'choice_d': 'The list of subcontractors on the project',
                'correct_answer': 'b',
            },
            {
                'order': 4,
                'text': 'When should a nonconformance report (NCR) be initiated?',
                'choice_a': 'Only after turnover is complete',
                'choice_b': 'When work, material, or documentation does not meet the specified requirement',
                'choice_c': 'Only when the client requests it',
                'choice_d': 'At the end of every shift regardless of findings',
                'correct_answer': 'b',
            },
            {
                'order': 5,
                'text': 'Before welding begins, which three items must be verified?',
                'choice_a': 'WPS posted, welder qualified, consumables matched to procedure',
                'choice_b': 'Welder name, shift schedule, weather forecast',
                'choice_c': 'Paint color, surface temperature, project budget',
                'choice_d': 'Crane certification, rigging plan, lift radius',
                'correct_answer': 'a',
            },
            {
                'order': 6,
                'text': 'What is the number-one cause of protective coating failure?',
                'choice_a': 'Using the wrong paint color',
                'choice_b': 'Applying coatings in direct sunlight',
                'choice_c': 'Inadequate surface preparation',
                'choice_d': 'Exceeding the maximum dry-film thickness',
                'correct_answer': 'c',
            },
            {
                'order': 7,
                'text': 'The five stages of the NCR lifecycle are:',
                'choice_a': 'Plan, Do, Check, Act, Close',
                'choice_b': 'Initiation, Evaluation, Disposition, Corrective Action, Closeout',
                'choice_c': 'Draft, Review, Approve, Issue, Archive',
                'choice_d': 'Identify, Quarantine, Test, Release, Report',
                'correct_answer': 'b',
            },
            {
                'order': 8,
                'text': 'What is the purpose of a traveler package?',
                'choice_a': 'To track employee travel expenses',
                'choice_b': 'To follow a component from receiving through installation to turnover',
                'choice_c': 'To schedule inspector site visits',
                'choice_d': 'To document safety incidents',
                'correct_answer': 'b',
            },
            {
                'order': 9,
                'text': 'When ambient conditions are outside specification limits during coating application, you should:',
                'choice_a': 'Proceed and apply an extra coat to compensate',
                'choice_b': 'Stop work and wait for conditions to return within limits',
                'choice_c': 'Reduce the coating thickness to speed up drying',
                'choice_d': 'Switch to a different coating system without engineering approval',
                'correct_answer': 'b',
            },
            {
                'order': 10,
                'text': 'What is the most common cause of turnover delays?',
                'choice_a': 'Equipment breakdowns',
                'choice_b': 'Weather interruptions',
                'choice_c': 'Missing or incomplete documentation',
                'choice_d': 'Labor shortages',
                'correct_answer': 'c',
            },
        ]

        for qd in questions:
            Question.objects.get_or_create(
                quiz=quiz, order=qd['order'],
                defaults={
                    'text': qd['text'],
                    'choice_a': qd['choice_a'],
                    'choice_b': qd['choice_b'],
                    'choice_c': qd['choice_c'],
                    'choice_d': qd['choice_d'],
                    'correct_answer': qd['correct_answer'],
                },
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # TEST USER
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        user, user_created = User.objects.get_or_create(
            email='test@fdq.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'profession': 'qc',
                'industry': 'gc',
                'company_name': 'Test Construction Co',
                'state': 'TX',
            },
        )
        if user_created:
            user.set_password('testpass123')
            user.save()

        Application.objects.get_or_create(
            user=user,
            defaults={
                'status': 'approved',
                'certifications_held': '',
                'additional_info': '',
                'reviewed_at': timezone.now(),
                'can_reapply': False,
            },
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # SUMMARY
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        module_count = Module.objects.filter(tier=tier).count()
        lesson_count = Lesson.objects.filter(module__tier=tier).count()
        exercise_count = InteractiveExercise.objects.filter(lesson__module__tier=tier).count()
        question_count = Question.objects.filter(quiz=quiz).count()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('── Summary ──'))
        self.stdout.write(f'Tier 1: {tier.name}')
        self.stdout.write(f'Tier 2: {tier2.name} (prerequisite: {tier2.prerequisite.name})')
        self.stdout.write(f'Tier 3: {tier3.name} (prerequisite: {tier3.prerequisite.name})')
        self.stdout.write(f'Modules: {module_count}')
        self.stdout.write(f'Lessons: {lesson_count} (including {exercise_count} interactive)')
        self.stdout.write(f'Exercises: {exercise_count}')
        self.stdout.write(f'Questions: {question_count}')

        for mod in Module.objects.filter(tier=tier).order_by('order'):
            gate = 'GATED' if mod.gate_required else 'open'
            mod_lessons = Lesson.objects.filter(module=mod).count()
            self.stdout.write(f'  Module {mod.order}: {mod.title} — {mod_lessons} lessons [{gate}]')

        self.stdout.write(f'Test user: test@fdq.com ({"created" if user_created else "already existed"})')
        self.stdout.write(f'Password: testpass123')
        self.stdout.write('')
        self.stdout.write(
            'Log in at /accounts/login/ with test@fdq.com / testpass123 '
            'and navigate to /certifications/ to test enrollment.'
        )
