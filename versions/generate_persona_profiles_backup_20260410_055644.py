"""
Generate detailed persona profiles for SMB and Commercial segments
Based on real Gong data analysis
"""

personas = {   'Commercial': {   'C-Suite Decision Maker': {   'buying_behavior': {   'authority_level': 'Ultimate - signs off on '
                                                                                              'budget',
                                                                           'committee_size': 'Final approver (reviews '
                                                                                             'deal packaged by team)',
                                                                           'decision_speed': 'Appears in week 6-8 of '
                                                                                             'deal',
                                                                           'prefers': 'Concise executive briefing, '
                                                                                      'peer references'},
                                                    'challenges': [   'Platform vs. point solution debate - prefer '
                                                                      'vendor consolidation',
                                                                      'Strategic investment - need 3-5 year vision',
                                                                      'Risk mitigation - big migrations are high '
                                                                      'stakes'],
                                                    'challenges_from_gong': [   'Platform vs. point solution debate - '
                                                                                'prefer vendor consolidation',
                                                                                'Strategic investment - need 3-5 year '
                                                                                'vision',
                                                                                'Risk mitigation - big migrations are '
                                                                                'high stakes'],
                                                    'content_preferences': [   'Board-ready business case',
                                                                               'Strategic roadmap briefings',
                                                                               'Industry analyst validation',
                                                                               'Executive roundtables with peers',
                                                                               'Financial analyst reports'],
                                                    'evaluation_criteria': [   'Strategic platform play - can this '
                                                                               'replace 3+ tools?',
                                                                               'Future-proof - AI roadmap, innovation '
                                                                               'velocity',
                                                                               'Vendor stability and financial health',
                                                                               'Implementation risk and timeline',
                                                                               'Executive sponsorship and support from '
                                                                               'vendor'],
                                                    'goals': [   'Platform consolidation - reduce vendor count',
                                                                 'Improve customer retention and LTV',
                                                                 'Enable profitable growth'],
                                                    'job_titles': ['COO', 'CEO', 'Chief Customer Officer', 'President'],
                                                    'key_messages': [   'Platform consolidation - replace 3-5 tools '
                                                                        'with one',
                                                                        'Proven at your scale - 1000+ mid-market '
                                                                        'customers',
                                                                        'AI-first roadmap - built for next 5 years',
                                                                        'Risk mitigation - phased rollout, rollback '
                                                                        'plans',
                                                                        'Buyers expect AI capabilities as default, not '
                                                                        'premium feature',
                                                                        'Need ROI justification and vendor risk docs '
                                                                        'upfront'],
                                                    'objections': [   '"Why not just keep what we have?"',
                                                                      '"What\'s the business case for this level of '
                                                                      'investment?"',
                                                                      '"What if this impacts customer experience '
                                                                      'during transition?"'],
                                                    'pain_points': [],
                                                    'prevalence': '54% of Commercial deals',
                                                    'reports_to': 'Board',
                                                    'role_in_deal': 'Budget Holder (appears late in process)',
                                                    'success_metrics': [   'Customer retention rate',
                                                                           'Support cost as % of revenue',
                                                                           'NPS',
                                                                           'Vendor consolidation savings',
                                                                           'Time to implement innovation'],
                                                    'team_size': 'Entire company (250-1,499 employees)'},
                      'CX Champion': {   'buying_behavior': {   'authority_level': 'Medium - needs buy-in from IT, '
                                                                                   'Finance, Ops',
                                                                'committee_size': '6-8 people (CX, IT, Ops, Finance, '
                                                                                  'Procurement, C-Suite)',
                                                                'decision_speed': '75-100 days',
                                                                'prefers': 'Structured evaluation, proof-of-concept, '
                                                                           'reference checks'},
                                         'challenges': [   'Integration complexity - custom dispatch systems, '
                                                           'multi-client data',
                                                           'Self-service culture shift - not just tools, behavioral '
                                                           'change',
                                                           'Reporting gaps - need custom dashboards for executives'],
                                         'challenges_from_gong': [   'Integration complexity - custom dispatch '
                                                                     'systems, multi-client data',
                                                                     'Self-service culture shift - not just tools, '
                                                                     'behavioral change',
                                                                     'Reporting gaps - need custom dashboards for '
                                                                     'executives'],
                                         'content_preferences': [   'Enterprise customer case studies',
                                                                    'Executive briefings with VP-level champions',
                                                                    'Analyst reports (Gartner Magic Quadrant)',
                                                                    'ROI models for mid-market',
                                                                    'Reference calls with similar companies'],
                                         'evaluation_criteria': [   'Enterprise scalability - can this handle 100+ '
                                                                    'agents and grow to 500?',
                                                                    'Advanced automation - intent-based routing, '
                                                                    'AI-powered triage',
                                                                    'Multi-org/multi-brand support',
                                                                    'Customization - workflows, fields, automations',
                                                                    'Change management support during rollout'],
                                         'goals': [   'Scale support operations across regions/brands',
                                                      'Drive 55-60% ticket deflection through self-service + AI',
                                                      'Improve CSAT while reducing cost-per-ticket'],
                                         'job_titles': [   'VP Customer Service',
                                                           'VP Customer Experience',
                                                           'Director of Customer Support',
                                                           'Head of Global Support',
                                                           'Senior Director CX'],
                                         'key_messages': [   'Built for enterprise complexity - multi-org, custom '
                                                             'workflows, advanced routing',
                                                             'Change management included - dedicated team to ensure '
                                                             'adoption',
                                                             'Phased rollout - start with one team, expand when ready',
                                                             'Agent-loved - 4.6★ rating, faster than legacy tools',
                                                             'Buyers expect AI capabilities as default, not premium '
                                                             'feature',
                                                             'Need ROI justification and vendor risk docs upfront'],
                                         'objections': [   '"We have too many custom requirements"',
                                                           '"Our team is already overwhelmed - can\'t handle a big '
                                                           'migration"',
                                                           '"How long will implementation really take?"'],
                                         'pain_points': [],
                                         'prevalence': '92% of Commercial deals',
                                         'reports_to': 'COO, Chief Customer Officer, or CEO',
                                         'role_in_deal': 'Primary Champion (but needs coalition)',
                                         'success_metrics': [   'CSAT / NPS',
                                                                'Ticket deflection rate (target: 55-60%)',
                                                                'Cost per ticket',
                                                                'First response time by tier',
                                                                'Agent utilization rate'],
                                         'team_size': '25-100 agents (often multi-region)'},
                      'Finance/Procurement Gatekeeper': {   'buying_behavior': {   'authority_level': 'High - can '
                                                                                                      'block deals',
                                                                                   'committee_size': 'Works with legal '
                                                                                                     'and finance',
                                                                                   'decision_speed': 'Gatekeeper (adds '
                                                                                                     '2-4 weeks)',
                                                                                   'prefers': 'Formal RFP process, '
                                                                                              'detailed financial '
                                                                                              'analysis'},
                                                            'challenges': [   'Procurement appearing 40% earlier - at '
                                                                              'demo stage, not just negotiation',
                                                                              'Formal RFP/RFI processes - need '
                                                                              'structured responses',
                                                                              'Vendor risk assessment requirements'],
                                                            'challenges_from_gong': [   'Procurement appearing 40% '
                                                                                        'earlier - at demo stage, not '
                                                                                        'just negotiation',
                                                                                        'Formal RFP/RFI processes - '
                                                                                        'need structured responses',
                                                                                        'Vendor risk assessment '
                                                                                        'requirements'],
                                                            'content_preferences': [   'RFP response templates',
                                                                                       'Vendor risk assessment '
                                                                                       'questionnaires',
                                                                                       'Financial statements and '
                                                                                       'stability proof',
                                                                                       'Pricing comparison matrices',
                                                                                       'Procurement peer references'],
                                                            'evaluation_criteria': [   'Total cost of ownership '
                                                                                       '(licensing, implementation, '
                                                                                       'training, support)',
                                                                                       'Contract terms (auto-renewal, '
                                                                                       'cancellation, SLAs, penalties)',
                                                                                       'Vendor financial stability '
                                                                                       '(Dun & Bradstreet, funding)',
                                                                                       'Pricing scalability (what '
                                                                                       'happens at 2x, 3x growth?)',
                                                                                       'Reference checks from '
                                                                                       'procurement peers'],
                                                            'goals': [   'Negotiate favorable contract terms',
                                                                         'Ensure compliance with procurement policies',
                                                                         'Vendor risk management and due diligence'],
                                                            'job_titles': [   'CFO',
                                                                              'VP Finance',
                                                                              'Procurement Director',
                                                                              'Vendor Management',
                                                                              'Director of Procurement'],
                                                            'key_messages': [   'Transparent pricing - no hidden fees, '
                                                                                'predictable scaling',
                                                                                'Flexible contract terms available for '
                                                                                'enterprises',
                                                                                'Financially stable - [funding status, '
                                                                                'customer count]',
                                                                                'TCO advantage - replace 3 tools, '
                                                                                'reduce implementation costs',
                                                                                'Buyers expect AI capabilities as '
                                                                                'default, not premium feature',
                                                                                'Need ROI justification and vendor '
                                                                                'risk docs upfront'],
                                                            'objections': [   '"Your pricing doesn\'t fit our budget '
                                                                              'model"',
                                                                              '"We need more favorable contract terms"',
                                                                              '"How do we know you\'ll be around in 5 '
                                                                              'years?"'],
                                                            'pain_points': [],
                                                            'prevalence': '58% of Commercial deals',
                                                            'reports_to': 'CEO or Board',
                                                            'role_in_deal': 'Gatekeeper (appears at demo stage, not '
                                                                            'just contracting)',
                                                            'success_metrics': [   'Cost savings vs. budget',
                                                                                   'Contract compliance',
                                                                                   'Vendor consolidation progress',
                                                                                   'Risk mitigation',
                                                                                   'Favorable payment terms achieved'],
                                                            'team_size': 'Finance/procurement team'},
                      'IT Influencer': {   'buying_behavior': {   'authority_level': 'High - can veto deals',
                                                                  'committee_size': 'Works with security team',
                                                                  'decision_speed': 'Involved at demo stage (week 2-3)',
                                                                  'prefers': 'Technical deep dives, proof-of-concept'},
                                           'challenges': [   'AI governance scrutiny - how is AI trained? Where is '
                                                             'data stored?',
                                                             'Data residency requirements (EU, APAC)',
                                                             'Enterprise integration complexity'],
                                           'challenges_from_gong': [   'AI governance scrutiny - how is AI trained? '
                                                                       'Where is data stored?',
                                                                       'Data residency requirements (EU, APAC)',
                                                                       'Enterprise integration complexity'],
                                           'content_preferences': [   'Security whitepapers',
                                                                      'Compliance certifications',
                                                                      'API documentation and sandbox',
                                                                      'Architecture diagrams',
                                                                      'Penetration test results (under NDA)'],
                                           'evaluation_criteria': [   '**#1 Priority:** Security & compliance (SOC 2 '
                                                                      'Type 2, ISO 27001, GDPR, HIPAA)',
                                                                      'API quality - RESTful, well-documented, '
                                                                      'versioned',
                                                                      'SSO/SAML, SCIM provisioning',
                                                                      'Data governance - encryption, residency, '
                                                                      'retention policies',
                                                                      'AI transparency - how models work, what data '
                                                                      'they use'],
                                           'goals': [   'Ensure enterprise-grade security and compliance',
                                                        'Manage integrations and API strategy',
                                                        'Minimize technical debt and shadow IT'],
                                           'job_titles': [   'VP IT',
                                                             'Director of IT',
                                                             'Head of Information Security',
                                                             'IT Manager',
                                                             'CISO'],
                                           'key_messages': [   'Enterprise security built-in - SOC 2 Type 2, ISO '
                                                               '27001, GDPR, HIPAA',
                                                               'AI governance - transparent models, customer data '
                                                               'isolation, audit trails',
                                                               'Enterprise APIs - RESTful, 99.9% uptime SLA, versioned',
                                                               'Data residency options - EU, APAC, US regions',
                                                               'Buyers expect AI capabilities as default, not premium '
                                                               'feature',
                                                               'Need ROI justification and vendor risk docs upfront'],
                                           'objections': [   '"How do you ensure AI doesn\'t expose sensitive customer '
                                                             'data?"',
                                                             '"Can you meet our data residency requirements?"',
                                                             '"What happens if your API changes and breaks our '
                                                             'integrations?"'],
                                           'pain_points': [],
                                           'prevalence': '85% of Commercial deals',
                                           'reports_to': 'CTO, COO, or CEO',
                                           'role_in_deal': 'Co-Champion & Validator (critical path)',
                                           'success_metrics': [   'Security audit pass rate',
                                                                  'Zero data breaches',
                                                                  'API uptime and reliability',
                                                                  'Integration stability',
                                                                  'Compliance certification maintenance'],
                                           'team_size': '5-25 IT staff'},
                      'Operations Leader': {   'buying_behavior': {   'authority_level': 'Medium-High - can influence '
                                                                                         'decision',
                                                                      'committee_size': 'Works closely with CX '
                                                                                        'Champion',
                                                                      'decision_speed': 'Influential throughout '
                                                                                        'process',
                                                                      'prefers': 'Operational deep dives, '
                                                                                 'metrics-focused demos'},
                                               'challenges': [   'WFM integration requirements - need to connect to '
                                                                 'existing tools',
                                                                 'Quality assurance at scale - AI needed',
                                                                 'Real-time operational dashboards'],
                                               'challenges_from_gong': [   'WFM integration requirements - need to '
                                                                           'connect to existing tools',
                                                                           'Quality assurance at scale - AI needed',
                                                                           'Real-time operational dashboards'],
                                               'content_preferences': [   'WFM integration guides',
                                                                          'QA automation case studies',
                                                                          'Operational efficiency benchmarks',
                                                                          'Workforce optimization ROI models'],
                                               'evaluation_criteria': [   'WFM capabilities or integrations (Verint, '
                                                                          'Calabrio, NICE)',
                                                                          'AI-powered QA to review 100% of '
                                                                          'interactions',
                                                                          'Real-time operational dashboards',
                                                                          'Agent performance management tools',
                                                                          'Customizable reporting for different '
                                                                          'stakeholders'],
                                               'goals': [   'Optimize workforce management and capacity planning',
                                                            'Scale QA from <1% to 100% of interactions (AI-powered)',
                                                            'Improve operational efficiency and reduce waste'],
                                               'job_titles': [   'Director of Service Operations',
                                                                 'VP Operations',
                                                                 'Workforce Management Manager',
                                                                 'Quality Assurance Director',
                                                                 'Service Delivery Manager'],
                                               'key_messages': [   'AI-powered QA - review 100% of interactions, not '
                                                                   'just 1%',
                                                                   'WFM integrations - Verint, Calabrio, NICE, custom '
                                                                   'APIs',
                                                                   'Real-time ops center - visibility into all teams',
                                                                   'Agent coaching tools - turn QA insights into '
                                                                   'performance gains',
                                                                   'Buyers expect AI capabilities as default, not '
                                                                   'premium feature',
                                                                   'Need ROI justification and vendor risk docs '
                                                                   'upfront'],
                                               'objections': [   '"Will this integrate with our WFM platform?"',
                                                                 '"Can your AI QA handle our complex quality rubrics?"',
                                                                 '"Is reporting flexible enough for our needs?"'],
                                               'pain_points': [],
                                               'prevalence': '45% of Commercial deals (EMERGING)',
                                               'reports_to': 'COO or CX Champion',
                                               'role_in_deal': 'Key Influencer (growing importance)',
                                               'success_metrics': [   'Schedule adherence %',
                                                                      'Occupancy rate',
                                                                      'QA score trends',
                                                                      'Cost per interaction',
                                                                      'Agent attrition rate'],
                                               'team_size': 'Oversees ops, WFM, QA teams'}},
    'Digital': {   'Customer Service Generalist': {   'buying_behavior': {   'authority_level': 'Low - influencer only',
                                                                             'committee_size': 'Needs founder approval',
                                                                             'decision_speed': 'Recommends to founder '
                                                                                               '(adds 1-2 weeks)',
                                                                             'prefers': 'Trial before pitching to '
                                                                                        'founder'},
                                                      'challenges': [   'Need omnichannel - customers reach out '
                                                                        'everywhere',
                                                                        'Knowledge base gaps - no organized help '
                                                                        'content',
                                                                        'No collaboration tools when teammates help'],
                                                      'challenges_from_gong': [   'Need omnichannel - customers reach '
                                                                                  'out everywhere',
                                                                                  'Knowledge base gaps - no organized '
                                                                                  'help content',
                                                                                  'No collaboration tools when '
                                                                                  'teammates help'],
                                                      'content_preferences': [   'Video walkthroughs',
                                                                                 'Getting started checklist',
                                                                                 'Templates for common responses',
                                                                                 'Small business case studies',
                                                                                 'Live onboarding help'],
                                                      'evaluation_criteria': [   'Easy to use daily - not intimidating',
                                                                                 'Handles email, chat, and social in '
                                                                                 'one place',
                                                                                 'Can create simple help articles',
                                                                                 'Affordable on tight budget',
                                                                                 'Quick to learn - ideally no training '
                                                                                 'needed'],
                                                      'goals': [   'Respond to customers quickly across email, chat, '
                                                                   'social',
                                                                   'Keep founder happy by handling support '
                                                                   'independently',
                                                                   'Track customer issues and spot patterns'],
                                                      'job_titles': [   'Customer Success Manager',
                                                                        'Office Manager',
                                                                        'Operations Coordinator',
                                                                        'Customer Service Rep'],
                                                      'key_messages': [   'All customer conversations in one inbox',
                                                                          'Built for small teams - dead simple to use',
                                                                          'Free help center builder included',
                                                                          'Get started in minutes, not hours',
                                                                          'Buyers expect AI capabilities as default, '
                                                                          'not premium feature',
                                                                          'Self-service setup and pre-built templates '
                                                                          'are critical'],
                                                      'objections': [   '"Will the founder approve the cost?"',
                                                                        '"Looks too complicated for our small team"',
                                                                        '"We already use email, why change?"'],
                                                      'pain_points': [],
                                                      'prevalence': '45% of Digital deals',
                                                      'reports_to': 'Founder/Owner',
                                                      'role_in_deal': 'User/Influencer (recommends to founder)',
                                                      'success_metrics': [   'Response time',
                                                                             'Number of conversations handled',
                                                                             'Customer satisfaction ratings',
                                                                             'Time saved with canned responses',
                                                                             'Help center article views'],
                                                      'team_size': 'Handles support solo or with 1-2 others'},
                   'Founder/Owner': {   'buying_behavior': {   'authority_level': 'Complete - no approvals needed',
                                                               'committee_size': '1 person (solo decision)',
                                                               'decision_speed': '7-14 days',
                                                               'prefers': 'Self-service trial, no sales calls, '
                                                                          'transparent pricing'},
                                        'challenges': [   'Price sensitivity - need startup/small business pricing',
                                                          'Self-service implementation required - no IT department',
                                                          'Mobile-first needs - managing support on the go'],
                                        'challenges_from_gong': [   'Price sensitivity - need startup/small business '
                                                                    'pricing',
                                                                    'Self-service implementation required - no IT '
                                                                    'department',
                                                                    'Mobile-first needs - managing support on the go'],
                                        'content_preferences': [   'Short video tutorials (2-3 minutes)',
                                                                   'Quick start guides',
                                                                   'Founder testimonials from similar businesses',
                                                                   'Pricing calculator',
                                                                   '14-day free trial'],
                                        'evaluation_criteria': [   'Price (must be under $50-100/month)',
                                                                   'Setup time (must be live in hours, not weeks)',
                                                                   'Mobile app quality',
                                                                   'No learning curve - intuitive like consumer apps',
                                                                   'Free trial to test before buying'],
                                        'goals': [   'Get support tools running quickly with zero IT help',
                                                     'Keep costs low - every dollar counts',
                                                     'Deliver professional customer service despite small team'],
                                        'job_titles': ['Founder', 'CEO', 'Owner', 'Managing Director'],
                                        'key_messages': [   'Special pricing for startups - as low as $19/month',
                                                            'Setup in 15 minutes - no technical skills required',
                                                            'Mobile app lets you support customers anywhere',
                                                            'Start free, pay as you grow',
                                                            'Buyers expect AI capabilities as default, not premium '
                                                            'feature',
                                                            'Self-service setup and pre-built templates are critical'],
                                        'objections': [   '"This is too expensive for our size"',
                                                          '"Looks complicated - don\'t have time to learn"',
                                                          '"Do I really need this or can I just use email?"'],
                                        'pain_points': [],
                                        'prevalence': '88% of Digital deals',
                                        'reports_to': 'Self',
                                        'role_in_deal': 'Sole Decision Maker',
                                        'success_metrics': [   'Time saved per day',
                                                               'Customer response time',
                                                               'Cost per month',
                                                               'Customer satisfaction',
                                                               'Tool adoption by team'],
                                        'team_size': '1-10 employees total'}},
    'Enterprise': {   'CX Executive': {   'buying_behavior': {   'authority_level': 'Executive Sponsor - drives but '
                                                                                    'needs coalition',
                                                                 'committee_size': '10-15 people (CX, IT, Finance, '
                                                                                   'Procurement, Legal, Security, '
                                                                                   'Operations)',
                                                                 'decision_speed': '6-12 months',
                                                                 'prefers': 'Structured RFP, POC with 50+ agents, '
                                                                            'multi-phase rollout'},
                                          'challenges': [   'Multi-year digital transformation roadmaps',
                                                            'Global rollout complexity - 5+ regions, compliance '
                                                            'requirements',
                                                            'Change management at scale - 100s of agents to train'],
                                          'challenges_from_gong': [   'Multi-year digital transformation roadmaps',
                                                                      'Global rollout complexity - 5+ regions, '
                                                                      'compliance requirements',
                                                                      'Change management at scale - 100s of agents to '
                                                                      'train'],
                                          'content_preferences': [   'Executive briefings with CCOs from similar '
                                                                     'companies',
                                                                     'Analyst reports (Gartner, Forrester, '
                                                                     'Constellation)',
                                                                     'Total Economic Impact study',
                                                                     'Multi-year transformation roadmap',
                                                                     'Board-ready business case'],
                                          'evaluation_criteria': [   'Enterprise scalability - proven at 1000+ agent '
                                                                     'deployments',
                                                                     'Strategic partnership - not just a vendor',
                                                                     'Global support - 24/7 enterprise SLAs, '
                                                                     'multi-language',
                                                                     'Gartner/Forrester positioning - top quadrant '
                                                                     'placement',
                                                                     'Change management & consulting services '
                                                                     'included'],
                                          'goals': [   'Transform customer experience into competitive advantage',
                                                       'Reduce cost-to-serve while improving NPS by 15+ points',
                                                       'Consolidate fragmented CX tech stack (8-15 tools)'],
                                          'job_titles': [   'SVP Customer Experience',
                                                            'Chief Customer Officer',
                                                            'VP Global Customer Support',
                                                            'Head of Customer Success & Support'],
                                          'key_messages': [   'Gartner Leader - proven at Fortune 500 scale',
                                                              'Migration de-risked - dedicated team, proven '
                                                              'methodology',
                                                              '18-24 month ROI with 25-30% efficiency gains',
                                                              'White-glove change management included',
                                                              'Buyers expect AI capabilities as default, not premium '
                                                              'feature',
                                                              'Need ROI justification and vendor risk docs upfront'],
                                          'objections': [   '"We\'ve already invested millions in our current '
                                                            'platform"',
                                                            '"Too risky to migrate 500+ agents"',
                                                            '"Our business is too complex for out-of-box solutions"'],
                                          'pain_points': [],
                                          'prevalence': '95% of Enterprise deals',
                                          'reports_to': 'CEO or President',
                                          'role_in_deal': 'Executive Sponsor & Final Approver',
                                          'success_metrics': [   'NPS improvement',
                                                                 'Cost-to-serve reduction',
                                                                 'Agent productivity (cases per agent)',
                                                                 'Platform consolidation (tools eliminated)',
                                                                 'Customer lifetime value impact'],
                                          'team_size': '100-500+ agents across multiple regions'},
                      'Enterprise IT Architect': {   'buying_behavior': {   'authority_level': 'Can block - must '
                                                                                               'approve architecture',
                                                                            'committee_size': 'IT architecture board '
                                                                                              '(5-8 people)',
                                                                            'decision_speed': '2-4 months technical '
                                                                                              'evaluation',
                                                                            'prefers': 'Technical POC, architecture '
                                                                                       'review, security assessment'},
                                                     'challenges': [   'Enterprise integration requirements - SSO, '
                                                                       'SCIM, APIs, webhooks',
                                                                       'Security and compliance - SOC 2, ISO, HIPAA, '
                                                                       'GDPR, FedRAMP',
                                                                       'Disaster recovery and business continuity '
                                                                       'planning'],
                                                     'challenges_from_gong': [   'Enterprise integration requirements '
                                                                                 '- SSO, SCIM, APIs, webhooks',
                                                                                 'Security and compliance - SOC 2, '
                                                                                 'ISO, HIPAA, GDPR, FedRAMP',
                                                                                 'Disaster recovery and business '
                                                                                 'continuity planning'],
                                                     'content_preferences': [   'Enterprise architecture diagrams',
                                                                                'Security and compliance documentation',
                                                                                'API and integration documentation',
                                                                                'Technical deep-dive sessions',
                                                                                'Reference architectures from similar '
                                                                                'enterprises'],
                                                     'evaluation_criteria': [   'Enterprise security certifications '
                                                                                '(SOC 2 Type 2, ISO 27001, FedRAMP)',
                                                                                'Integration architecture - REST APIs, '
                                                                                'webhooks, SCIM, enterprise SSO',
                                                                                'Scalability and performance - SLAs '
                                                                                'for 99.99% uptime',
                                                                                'Data governance - encryption, '
                                                                                'residency, retention',
                                                                                'Professional services team for '
                                                                                'complex implementations'],
                                                     'goals': [   'Ensure enterprise architecture alignment and '
                                                                  'standards',
                                                                  'Reduce technical debt and platform sprawl',
                                                                  'Maintain security, compliance, and governance'],
                                                     'job_titles': [   'Enterprise Architect',
                                                                       'VP Technology',
                                                                       'Chief Information Officer',
                                                                       'Director Enterprise Applications'],
                                                     'key_messages': [   'Enterprise-grade security - SOC 2 Type 2, '
                                                                         'ISO 27001, FedRAMP authorized',
                                                                         'Pre-built enterprise integrations - SAP, '
                                                                         'Oracle, ServiceNow',
                                                                         '99.99% uptime SLA with enterprise support',
                                                                         'Global data residency options (US, EU, APAC)',
                                                                         'Buyers expect AI capabilities as default, '
                                                                         'not premium feature',
                                                                         'Need ROI justification and vendor risk docs '
                                                                         'upfront'],
                                                     'objections': [   '"Does this meet our enterprise security '
                                                                       'standards?"',
                                                                       '"How will this integrate with our '
                                                                       'SAP/Oracle/ServiceNow environment?"',
                                                                       '"What\'s the total cost of implementation and '
                                                                       'maintenance?"'],
                                                     'pain_points': [],
                                                     'prevalence': '85% of Enterprise deals',
                                                     'reports_to': 'CIO or CTO',
                                                     'role_in_deal': 'Technical Approver & Gatekeeper',
                                                     'success_metrics': [   'System uptime and performance',
                                                                            'Security audit pass rate',
                                                                            'Integration stability',
                                                                            'IT ticket reduction',
                                                                            'Platform consolidation achieved'],
                                                     'team_size': 'IT department of 50-200+'},
                      'Global Operations Leader': {   'buying_behavior': {   'authority_level': 'High influence - '
                                                                                                'operational approval '
                                                                                                'critical',
                                                                             'committee_size': 'Works with CX '
                                                                                               'Executive and regional '
                                                                                               'leaders',
                                                                             'decision_speed': '3-6 months evaluation',
                                                                             'prefers': 'Operational deep dives, '
                                                                                        'metrics analysis, phased POC'},
                                                      'challenges': [   'Advanced workforce management - AI '
                                                                        'forecasting, skills-based routing',
                                                                        'Quality management at scale - automated QA, '
                                                                        'coaching workflows',
                                                                        'Global process standardization across '
                                                                        'regions'],
                                                      'challenges_from_gong': [   'Advanced workforce management - AI '
                                                                                  'forecasting, skills-based routing',
                                                                                  'Quality management at scale - '
                                                                                  'automated QA, coaching workflows',
                                                                                  'Global process standardization '
                                                                                  'across regions'],
                                                      'content_preferences': [   'Operational metrics case studies',
                                                                                 'WFM integration documentation',
                                                                                 'Global deployment playbooks',
                                                                                 'ROI calculator for enterprise scale',
                                                                                 'Ops leader peer references'],
                                                      'evaluation_criteria': [   'Workforce management capabilities or '
                                                                                 'integrations',
                                                                                 'Quality assurance and coaching tools '
                                                                                 'at scale',
                                                                                 'Global reporting and real-time '
                                                                                 'dashboards',
                                                                                 'Automation capabilities - routing, '
                                                                                 'triage, responses',
                                                                                 'Proven ROI from similar-sized '
                                                                                 'deployments'],
                                                      'goals': [   'Optimize global workforce across time zones and '
                                                                   'regions',
                                                                   'Drive operational excellence - 95%+ SLA compliance',
                                                                   'Reduce operational costs by 20-30%'],
                                                      'job_titles': [   'VP Global Operations',
                                                                        'SVP Service Delivery',
                                                                        'Head of Workforce Management',
                                                                        'Director Global Support Operations'],
                                                      'key_messages': [   'Enterprise WFM integration - Nice, Verint, '
                                                                          'Calabrio',
                                                                          'AI-powered quality management - review 100% '
                                                                          'of interactions',
                                                                          'Global deployment proven - 20+ languages, '
                                                                          'all time zones',
                                                                          '25-30% efficiency gains within 12 months',
                                                                          'Buyers expect AI capabilities as default, '
                                                                          'not premium feature',
                                                                          'Need ROI justification and vendor risk docs '
                                                                          'upfront'],
                                                      'objections': [   '"Our operations are too complex for standard '
                                                                        'solutions"',
                                                                        '"Will this work across our 12 global sites?"',
                                                                        '"How long until we see efficiency gains?"'],
                                                      'pain_points': [],
                                                      'prevalence': '72% of Enterprise deals',
                                                      'reports_to': 'CX Executive or COO',
                                                      'role_in_deal': 'Key Influencer - operational approval needed',
                                                      'success_metrics': [   'SLA compliance rate',
                                                                             'Cost per interaction',
                                                                             'Agent utilization rate',
                                                                             'Quality assurance scores',
                                                                             'Workforce efficiency gains'],
                                                      'team_size': 'Oversees 100-500+ agents globally'}},
    'SMB': {   'C-Suite Decision Maker': {   'buying_behavior': {   'authority_level': 'Ultimate - final say on budget',
                                                                    'committee_size': '2-3 (CEO, CX Champion, '
                                                                                      'sometimes CFO)',
                                                                    'decision_speed': 'Fast (30-60 days once engaged)',
                                                                    'prefers': 'Concise business case, minimal '
                                                                               'meetings'},
                                             'challenges': [   "Scaling challenges - can't keep hiring agents to "
                                                               'handle volume',
                                                               'Lack of automation - too much manual work',
                                                               'Poor customer experience hurting brand reputation'],
                                             'challenges_from_gong': [   "Scaling challenges - can't keep hiring "
                                                                         'agents to handle volume',
                                                                         'Lack of automation - too much manual work',
                                                                         'Poor customer experience hurting brand '
                                                                         'reputation'],
                                             'content_preferences': [   'Executive briefings (15 min max)',
                                                                        'ROI case studies from similar companies',
                                                                        'Analyst reports (Gartner, Forrester)',
                                                                        'Board-ready business case templates',
                                                                        'CFO-approved pricing models'],
                                             'evaluation_criteria': [   '**#1 Priority:** Clear ROI - will this help '
                                                                        'us grow without adding headcount?',
                                                                        'Total cost of ownership (not just license '
                                                                        'cost)',
                                                                        'Implementation risk - can we do this without '
                                                                        'disrupting business?',
                                                                        'Scalability - will this grow with us to 500 '
                                                                        'employees?',
                                                                        'Vendor stability - is this company going to '
                                                                        'be around?'],
                                             'goals': [   'Enable company growth without proportional headcount '
                                                          'increases',
                                                          'Improve customer satisfaction and retention',
                                                          'Operational efficiency - do more with less'],
                                             'job_titles': ['CEO', 'COO', 'President', 'Founder'],
                                             'key_messages': [   'Grow support capacity 2x without doubling headcount '
                                                                 '(AI + automation)',
                                                                 'Predictable pricing - no surprise costs as you scale',
                                                                 'Fast implementation = minimal business disruption',
                                                                 'Proven ROI: customers see 30% productivity gains in '
                                                                 '90 days',
                                                                 'Buyers expect AI capabilities as default, not '
                                                                 'premium feature',
                                                                 'Self-service setup and pre-built templates are '
                                                                 'critical'],
                                             'objections': [   '"How do I know this will actually improve our '
                                                               'metrics?"',
                                                               '"What if implementation goes wrong and our support '
                                                               'grinds to a halt?"',
                                                               '"Can we really afford this in this economy?"'],
                                             'pain_points': [],
                                             'prevalence': '68% of SMB deals',
                                             'reports_to': 'Board or self (Owner)',
                                             'role_in_deal': 'Budget Holder & Final Approver',
                                             'success_metrics': [   'Cost per ticket',
                                                                    'Support cost as % of revenue',
                                                                    'Customer retention rate',
                                                                    'NPS',
                                                                    'Agent headcount vs. ticket volume ratio'],
                                             'team_size': 'Entire company (50-249 employees)'},
               'CX Champion': {   'buying_behavior': {   'authority_level': 'High - can often drive decision with '
                                                                            'C-Suite approval',
                                                         'committee_size': '3-4 people (CX Champion, C-Suite, Finance, '
                                                                           'sometimes IT)',
                                                         'decision_speed': '45-60 days',
                                                         'prefers': 'Fast-moving pilots over long enterprise sales '
                                                                    'cycles'},
                                  'challenges': [   'Integration gaps - switching between Zendesk, CRM, and 3+ other '
                                                    'tools',
                                                    'Incomplete help center - lacking self-service articles',
                                                    'No AI/automation - manually routing and responding to every '
                                                    'ticket'],
                                  'challenges_from_gong': [   'Integration gaps - switching between Zendesk, CRM, and '
                                                              '3+ other tools',
                                                              'Incomplete help center - lacking self-service articles',
                                                              'No AI/automation - manually routing and responding to '
                                                              'every ticket'],
                                  'content_preferences': [   'Customer testimonials from similar-sized companies',
                                                             'Quick demo videos (5-10 min)',
                                                             'ROI calculators',
                                                             'Implementation timelines',
                                                             'Free trial or POC to test with team'],
                                  'evaluation_criteria': [   '**#1 Priority:** Ease of implementation & time to value '
                                                             '(want live in 2-4 weeks)',
                                                             'Simple, intuitive interface agents can learn in days',
                                                             'Out-of-box integrations with existing tools (Salesforce, '
                                                             'Slack)',
                                                             'Clear ROI story - ticket deflection, faster resolution '
                                                             'times',
                                                             'Responsive support during onboarding'],
                                  'goals': [   'Reduce agent handle time and improve productivity',
                                               'Meet or exceed SLA targets (1-4 hour first response)',
                                               'Improve CSAT/NPS scores'],
                                  'job_titles': [   'VP Customer Service',
                                                    'Director of Customer Support',
                                                    'Head of Customer Experience',
                                                    'Customer Service Manager',
                                                    'Support Manager'],
                                  'key_messages': [   'Live in 2 weeks with minimal IT involvement',
                                                      'Agents love it - 4.5★ ease of use rating',
                                                      'Agent productivity up 30% in first 90 days (via automation)',
                                                      'Self-service deflects 30-40% of tickets automatically',
                                                      'Buyers expect AI capabilities as default, not premium feature',
                                                      'Self-service setup and pre-built templates are critical'],
                                  'objections': [   '"We don\'t have time for a long implementation"',
                                                    '"Our agents are already learning too many new tools"',
                                                    '"We tried AI before and it gave wrong answers to customers"'],
                                  'pain_points': [],
                                  'prevalence': '98% of SMB deals',
                                  'reports_to': 'COO or CEO',
                                  'role_in_deal': 'Primary Champion & Decision Driver',
                                  'success_metrics': [   'First response time (target: <1 hour)',
                                                         'CSAT score',
                                                         'Ticket volume & deflection rate',
                                                         'Agent productivity (tickets per agent per day)',
                                                         'Time to resolution'],
                                  'team_size': '5-25 agents'},
               'Finance/Procurement Gatekeeper': {   'buying_behavior': {   'authority_level': 'High - can block deals',
                                                                            'committee_size': 'Solo review or with CEO',
                                                                            'decision_speed': 'Gatekeeper (adds 1-2 '
                                                                                              'weeks)',
                                                                            'prefers': 'Financial analysis, minimal '
                                                                                       'sales fluff'},
                                                     'challenges': [   'Economic sensitivity - longer approval cycles, '
                                                                       'more scrutiny',
                                                                       'Preference for monthly/quarterly payment terms '
                                                                       '(cash flow)',
                                                                       'ROI justification requirements increasing'],
                                                     'challenges_from_gong': [   'Economic sensitivity - longer '
                                                                                 'approval cycles, more scrutiny',
                                                                                 'Preference for monthly/quarterly '
                                                                                 'payment terms (cash flow)',
                                                                                 'ROI justification requirements '
                                                                                 'increasing'],
                                                     'content_preferences': [   'ROI calculators',
                                                                                'TCO comparisons',
                                                                                'Pricing guides',
                                                                                'Payment terms options',
                                                                                'Reference customers with similar '
                                                                                'budget profiles'],
                                                     'evaluation_criteria': [   'Total cost of ownership (license + '
                                                                                'implementation + training)',
                                                                                'Payment terms flexibility (monthly '
                                                                                'vs. annual)',
                                                                                'ROI evidence from similar companies',
                                                                                'Contract terms (auto-renewal, '
                                                                                'cancellation policy)',
                                                                                'Price predictability as we scale'],
                                                     'goals': [   'Control costs and maintain budget discipline',
                                                                  'Ensure ROI on technology investments',
                                                                  'Predictable, manageable cash flow'],
                                                     'job_titles': [   'CFO',
                                                                       'Finance Director',
                                                                       'Controller',
                                                                       'VP Finance'],
                                                     'key_messages': [   'Clear ROI: 30% productivity gain = 5-6 month '
                                                                         'payback',
                                                                         'Flexible payment terms available',
                                                                         'Predictable per-agent pricing - no surprise '
                                                                         'fees',
                                                                         'Cheaper than hiring: one agent salary = 10+ '
                                                                         'licenses',
                                                                         'Buyers expect AI capabilities as default, '
                                                                         'not premium feature',
                                                                         'Self-service setup and pre-built templates '
                                                                         'are critical'],
                                                     'objections': [   '"Can we really afford this right now?"',
                                                                       '"What\'s the payback period?"',
                                                                       '"Why is this better than just hiring another '
                                                                       'agent?"'],
                                                     'pain_points': [],
                                                     'prevalence': '42% of SMB deals',
                                                     'reports_to': 'CEO or Board',
                                                     'role_in_deal': 'Budget Approver',
                                                     'success_metrics': [   'Cost per ticket',
                                                                            'Support cost as % of revenue',
                                                                            'Payback period',
                                                                            'Avoided hiring costs',
                                                                            'Vendor consolidation savings'],
                                                     'team_size': 'Finance team (2-10 people)'},
               'IT Influencer': {   'buying_behavior': {   'authority_level': 'Advisory - can flag risks but rarely '
                                                                              'blocks',
                                                           'committee_size': 'Solo or with CISO',
                                                           'decision_speed': 'Quick review (1-2 weeks)',
                                                           'prefers': 'Technical documentation, sandbox access'},
                                    'challenges': [   'Security concerns even in SMB (SOC 2, encryption, SSO)',
                                                      'Integration requirements - need to connect to existing stack',
                                                      "Limited IT resources - can't support complex implementations"],
                                    'challenges_from_gong': [   'Security concerns even in SMB (SOC 2, encryption, '
                                                                'SSO)',
                                                                'Integration requirements - need to connect to '
                                                                'existing stack',
                                                                "Limited IT resources - can't support complex "
                                                                'implementations'],
                                    'content_preferences': [   'Security whitepapers',
                                                               'API documentation',
                                                               'Integration guides',
                                                               'Architecture diagrams',
                                                               'Compliance certifications'],
                                    'evaluation_criteria': [   'Security certifications (SOC 2 Type 2, ISO 27001)',
                                                               'SSO support (SAML, Okta, Azure AD)',
                                                               'API quality and documentation',
                                                               'Pre-built integrations vs. custom development needs',
                                                               'IT support load - how much will this require from our '
                                                               'team?'],
                                    'goals': [   'Ensure security and compliance (SOC 2, data encryption)',
                                                 'Minimize IT support burden - want tools that "just work"',
                                                 'Protect existing infrastructure investments'],
                                    'job_titles': [   'IT Manager',
                                                      'Head of IT',
                                                      'Director of IT',
                                                      'Systems Administrator'],
                                    'key_messages': [   'Enterprise-grade security built in (SOC 2, SSO, encryption)',
                                                        'Zero IT burden - cloud-hosted, auto-updates, 99.9% uptime',
                                                        'Pre-built integrations with 1000+ tools',
                                                        'Robust APIs for custom workflows',
                                                        'Buyers expect AI capabilities as default, not premium feature',
                                                        'Self-service setup and pre-built templates are critical'],
                                    'objections': [   '"Does this meet our security requirements?"',
                                                      '"How much custom development will we need?"',
                                                      '"What happens if the integration breaks?"'],
                                    'pain_points': [],
                                    'prevalence': '30% of SMB deals',
                                    'reports_to': 'COO, CEO, or CTO',
                                    'role_in_deal': 'Advisor & Validator (not blocker)',
                                    'success_metrics': [   'Security audit pass rate',
                                                           'System uptime',
                                                           'Integration stability',
                                                           'IT support tickets related to the tool',
                                                           'User provisioning time'],
                                    'team_size': '1-5 IT staff'},
               'Operations Leader': {   'buying_behavior': {   'authority_level': 'Low - provides input to CX Champion',
                                                               'committee_size': 'Consulted when present',
                                                               'decision_speed': 'N/A - not decision maker',
                                                               'prefers': 'Detailed operational demos'},
                                        'challenges': [   'Workforce management gaps - scheduling, forecasting',
                                                          "Quality assurance limitations - can't review at scale",
                                                          'Reporting fragmented across multiple tools'],
                                        'challenges_from_gong': [   'Workforce management gaps - scheduling, '
                                                                    'forecasting',
                                                                    "Quality assurance limitations - can't review at "
                                                                    'scale',
                                                                    'Reporting fragmented across multiple tools'],
                                        'content_preferences': [   'WFM integration guides',
                                                                   'QA best practices',
                                                                   'Operational metrics benchmarks',
                                                                   'Process optimization case studies'],
                                        'evaluation_criteria': [   'WFM capabilities or integrations',
                                                                   'QA and coaching tools',
                                                                   'Reporting and analytics depth',
                                                                   'Real-time operational dashboards',
                                                                   'Process automation capabilities'],
                                        'goals': [   'Optimize agent scheduling and capacity planning',
                                                     'Improve quality assurance and coaching',
                                                     'Reduce operational costs'],
                                        'job_titles': [   'Operations Manager',
                                                          'Service Delivery Manager',
                                                          'Director of Operations'],
                                        'key_messages': [   'Built-in QA tools to review 100% of interactions '
                                                            '(AI-powered)',
                                                            'Integrates with WFM platforms (Calabrio, Verint, etc.)',
                                                            'Real-time operational dashboards',
                                                            'Agent performance analytics and coaching tools',
                                                            'Buyers expect AI capabilities as default, not premium '
                                                            'feature',
                                                            'Self-service setup and pre-built templates are critical'],
                                        'objections': [   '"We already have WFM tools - will this integrate?"',
                                                          '"Can this handle our QA workflows?"',
                                                          '"Is the reporting customizable enough?"'],
                                        'pain_points': [],
                                        'prevalence': '22% of SMB deals',
                                        'reports_to': 'COO or CX Champion',
                                        'role_in_deal': 'Influencer (when present)',
                                        'success_metrics': [   'Schedule adherence',
                                                               'Occupancy rate',
                                                               'QA score trends',
                                                               'Process cycle time',
                                                               'Operational cost per ticket'],
                                        'team_size': 'Oversees support ops + WFM'}}}

# Generate markdown profiles
md_output = """# Buyer Persona Profiles - All Segments
**Based on 100,183 Gong calls | Q1 2026**
**Customer Service Focus: 95,036 calls analyzed**

---

"""

for segment in ['Digital', 'SMB', 'Commercial', 'Enterprise']:
    md_output += f"\n# {segment} SEGMENT PERSONAS\n\n"
    md_output += f"**Company Size:** {('50-249 employees' if segment == 'SMB' else '250-1,499 employees')}\n\n"
    md_output += "---\n\n"

    for persona_name, persona_data in personas[segment].items():
        md_output += f"\n## {persona_name}\n\n"

        # Header info
        md_output += "### Profile Overview\n\n"
        md_output += f"**Job Titles:** {', '.join(persona_data['job_titles'])}\n\n"
        md_output += f"**Reports To:** {persona_data['reports_to']}\n\n"
        md_output += f"**Team Size:** {persona_data['team_size']}\n\n"
        md_output += f"**Prevalence in Deals:** {persona_data['prevalence']}\n\n"
        md_output += f"**Role in Buying Process:** {persona_data['role_in_deal']}\n\n"

        # Goals
        md_output += "### Goals & Priorities\n\n"
        for goal in persona_data['goals']:
            md_output += f"- {goal}\n"
        md_output += "\n"

        # Pain points
        md_output += "### Pain Points\n\n"
        for pain in persona_data['pain_points']:
            md_output += f"- {pain}\n"
        md_output += "\n"

        # Challenges from Gong
        md_output += "### Customer Service Challenges (from Gong data)\n\n"
        for challenge in persona_data['challenges_from_gong']:
            md_output += f"- {challenge}\n"
        md_output += "\n"

        # Evaluation criteria
        md_output += "### How They Evaluate Solutions\n\n"
        for criterion in persona_data['evaluation_criteria']:
            md_output += f"{criterion}\n\n"

        # Objections
        md_output += "### Common Objections\n\n"
        for objection in persona_data['objections']:
            md_output += f"- {objection}\n"
        md_output += "\n"

        # Key messages
        md_output += "### Key Messages That Resonate\n\n"
        for message in persona_data['key_messages']:
            md_output += f"- {message}\n"
        md_output += "\n"

        # Content preferences
        md_output += "### Content Preferences\n\n"
        for content in persona_data['content_preferences']:
            md_output += f"- {content}\n"
        md_output += "\n"

        # Success metrics
        md_output += "### Success Metrics They Care About\n\n"
        for metric in persona_data['success_metrics']:
            md_output += f"- {metric}\n"
        md_output += "\n"

        # Buying behavior
        md_output += "### Buying Behavior\n\n"
        bb = persona_data['buying_behavior']
        md_output += f"**Decision Speed:** {bb['decision_speed']}\n\n"
        md_output += f"**Committee Size:** {bb['committee_size']}\n\n"
        md_output += f"**Authority Level:** {bb['authority_level']}\n\n"
        md_output += f"**Prefers:** {bb['prefers']}\n\n"

        md_output += "---\n\n"

# Save markdown
with open('/Users/chris.sherman/persona_analysis/reports/Persona_Profiles_Detailed.md', 'w') as f:
    f.write(md_output)

print("✓ Detailed persona profiles generated")
print("  Location: /Users/chris.sherman/persona_analysis/reports/Persona_Profiles_Detailed.md")
