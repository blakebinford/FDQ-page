from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from applications.models import Application
from lms.models import Tier, Module, Lesson, Quiz, Question


class Command(BaseCommand):
    help = 'Create dummy data for local development and testing.'

    def handle(self, *args, **options):
        # ── TIER ──
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
        self.stdout.write(f'Tier: {"created" if tier_created else "found"} — {tier.name}')

        # ── MODULE 1 ──
        mod1, _ = Module.objects.get_or_create(
            tier=tier, order=1,
            defaults={'title': 'Field Quality Fundamentals'},
        )

        # ── MODULE 1 LESSONS ──
        lessons_m1 = [
            {
                'order': 1,
                'title': 'What is Field-Driven Quality',
                'estimated_minutes': 5,
                'body': (
                    '<p>Field-Driven Quality (FDQ) is a systematic approach to '
                    'quality management that starts at the point of installation, '
                    'not in the office. It empowers field personnel — from welders '
                    'and pipefitters to inspectors and foremen — to own quality '
                    'outcomes on every task they touch.</p>'
                    '<p>Traditional quality programs rely on after-the-fact '
                    'inspection. FDQ flips that model: the crew building the work '
                    'is also the first line of quality assurance. When the people '
                    'doing the work understand <em>why</em> each quality hold '
                    'point exists, rework rates drop and schedule confidence '
                    'improves.</p>'
                    '<p>This course will teach you how to apply FDQ principles '
                    'on active job sites, from pre-task planning through final '
                    'turnover documentation.</p>'
                ),
            },
            {
                'order': 2,
                'title': 'Pre-Task Quality Checks',
                'estimated_minutes': 8,
                'body': (
                    '<p>Every quality defect that reaches final inspection '
                    'started as a missed step before work began. Pre-task quality '
                    'checks are your first opportunity to prevent rework by '
                    'verifying materials, procedures, and environmental '
                    'conditions before the crew starts.</p>'
                    '<p>A pre-task check covers four areas: material '
                    'traceability (are the correct MTRs on hand?), procedure '
                    'review (does the crew have the current revision of the WPS '
                    'or installation procedure?), tooling and calibration (are '
                    'torque wrenches and gauges within their calibration window?), '
                    'and environmental conditions (is it too cold to pour grout, '
                    'or too humid for coating application?).</p>'
                    '<p>Document the results on the pre-task checklist and '
                    'obtain the required sign-offs before releasing the crew to '
                    'begin work. A five-minute check at the start prevents hours '
                    'of corrective action later.</p>'
                ),
            },
            {
                'order': 3,
                'title': 'Reading Field Documentation',
                'estimated_minutes': 6,
                'body': (
                    '<p>Field documentation is the written record that proves '
                    'work was performed correctly. The three documents you will '
                    'encounter most often are Inspection and Test Plans (ITPs), '
                    'checklists, and traveler packages.</p>'
                    '<p>An ITP is the master roadmap for every quality activity '
                    'on a scope of work. It lists each inspection point, the '
                    'acceptance criteria, who is responsible for performing the '
                    'check, and whether a hold or witness point applies. '
                    'Checklists break a single ITP line item into granular steps '
                    'the inspector walks through in the field.</p>'
                    '<p>A traveler package follows a component from receiving '
                    'through installation to turnover. It collects the MTR, fit-up '
                    'inspection record, NDE report, and final sign-off into one '
                    'bundle. Learning to read — and properly complete — these '
                    'documents is essential to field quality.</p>'
                ),
            },
            {
                'order': 4,
                'title': 'Identifying and Flagging Risks',
                'estimated_minutes': 7,
                'body': (
                    '<p>Risk identification in the field is not about '
                    'paperwork — it is about recognizing conditions that could '
                    'lead to nonconforming work <em>before</em> they do. Common '
                    'risk indicators include material substitutions, procedure '
                    'deviations, untrained personnel performing critical tasks, '
                    'and environmental conditions outside specification.</p>'
                    '<p>When you identify a risk, the escalation path depends on '
                    'severity. Minor deviations may be resolved with the crew '
                    'lead on the spot. Conditions that could affect structural '
                    'integrity or code compliance require a formal '
                    'nonconformance report (NCR) and a stop-work discussion '
                    'with the quality manager.</p>'
                    '<p>Never let schedule pressure override a legitimate '
                    'quality concern. Flagging a risk early is always less '
                    'expensive than discovering it during turnover or, worse, '
                    'after the facility is in service.</p>'
                ),
            },
        ]

        for ld in lessons_m1:
            Lesson.objects.get_or_create(
                module=mod1, order=ld['order'],
                defaults={
                    'title': ld['title'],
                    'content_type': 'reading',
                    'estimated_minutes': ld['estimated_minutes'],
                    'body': ld['body'],
                },
            )

        # ── MODULE 2 ──
        mod2, _ = Module.objects.get_or_create(
            tier=tier, order=2,
            defaults={'title': 'Inspection and Documentation'},
        )

        # ── MODULE 2 LESSONS ──
        lessons_m2 = [
            {
                'order': 5,
                'title': 'Weld Inspection Basics',
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
            {
                'order': 6,
                'title': 'Coating and Surface Prep',
                'estimated_minutes': 8,
                'body': (
                    '<p>Protective coatings fail for one reason more than any '
                    'other: inadequate surface preparation. Whether the '
                    'specification calls for SSPC-SP 6 (commercial blast), '
                    'SP 10 (near-white), or SP 5 (white metal), the standard '
                    'must be met and verified before the first coat is '
                    'applied.</p>'
                    '<p>Before blasting, confirm that the ambient temperature is '
                    'at least 5 °F above the dew point, relative humidity is '
                    'within the coating manufacturer\'s limits, and compressed '
                    'air is oil- and moisture-free. After blasting, measure the '
                    'surface profile with replica tape or a digital gauge and '
                    'compare it to the coating data sheet range.</p>'
                    '<p>Coating application requires wet-film thickness checks '
                    'during application and dry-film thickness verification after '
                    'cure. Document each coat — primer, intermediate, topcoat — '
                    'with batch numbers, mil readings, and environmental '
                    'conditions at time of application.</p>'
                ),
            },
            {
                'order': 7,
                'title': 'NCR Lifecycle',
                'estimated_minutes': 7,
                'body': (
                    '<p>A nonconformance report (NCR) documents any condition '
                    'where work, material, or documentation does not meet the '
                    'specified requirement. NCRs are not punitive — they are the '
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
            {
                'order': 8,
                'title': 'Turnover Documentation',
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
                    '<p>Start assembling packages early — do not wait until '
                    'mechanical completion. Assign a document controller to '
                    'track completion status by system, and conduct weekly '
                    'reviews to identify gaps while there is still time to '
                    'recover records from the field.</p>'
                ),
            },
        ]

        for ld in lessons_m2:
            Lesson.objects.get_or_create(
                module=mod2, order=ld['order'],
                defaults={
                    'title': ld['title'],
                    'content_type': 'reading',
                    'estimated_minutes': ld['estimated_minutes'],
                    'body': ld['body'],
                },
            )

        # ── QUIZ ──
        quiz, _ = Quiz.objects.get_or_create(
            tier=tier,
            defaults={
                'title': 'FDQ Practitioner Assessment',
                'passing_score': 80,
            },
        )

        # ── QUESTIONS ──
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

        # ── TEST USER ──
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

        # ── APPROVED APPLICATION ──
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

        # ── SUMMARY ──
        module_count = Module.objects.filter(tier=tier).count()
        lesson_count = Lesson.objects.filter(module__tier=tier).count()
        question_count = Question.objects.filter(quiz=quiz).count()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('── Summary ──'))
        self.stdout.write(f'Tier: {tier.name} ({"created" if tier_created else "already existed"})')
        self.stdout.write(f'Modules: {module_count}')
        self.stdout.write(f'Lessons: {lesson_count}')
        self.stdout.write(f'Questions: {question_count}')
        self.stdout.write(f'Test user: test@fdq.com ({"created" if user_created else "already existed"})')
        self.stdout.write(f'Password: testpass123')
        self.stdout.write('')
        self.stdout.write(
            'Log in at /accounts/login/ with test@fdq.com / testpass123 '
            'and navigate to /certifications/ to test enrollment.'
        )
