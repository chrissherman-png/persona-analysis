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
                                                    'pain_points': [   'Support org using 5-10 different tools '
                                                                       '(fragmented)',
                                                                       'Customer churn tied to poor support experience',
                                                                       "Can't get clear visibility into support "
                                                                       'operations'],
                                                    'prevalence': '54% of Commercial deals',
                                                    'recommended_products': [   {   'addresses_challenge': "I can't "
                                                                                                           'show the '
                                                                                                           'board what '
                                                                                                           'our '
                                                                                                           'support '
                                                                                                           'organization '
                                                                                                           'is '
                                                                                                           'actually '
                                                                                                           'delivering '
                                                                                                           '- we need '
                                                                                                           'real-time '
                                                                                                           'metrics',
                                                                                    'product': 'Analytics',
                                                                                    'relevance': 'High',
                                                                                    'url': 'https://www.zendesk.com/service/analytics/',
                                                                                    'why': 'Board wants proof support '
                                                                                           'investments are working. '
                                                                                           'Without executive '
                                                                                           'dashboards showing ROI, '
                                                                                           'support is seen as a cost '
                                                                                           'center, not a strategic '
                                                                                           'asset.',
                                                                                    'zendesk_name': 'Zendesk Explore'},
                                                                                {   'addresses_challenge': 'We need to '
                                                                                                           'consolidate '
                                                                                                           'vendors - '
                                                                                                           'managing '
                                                                                                           'five '
                                                                                                           'different '
                                                                                                           'support '
                                                                                                           'tools is '
                                                                                                           'costing us '
                                                                                                           'money and '
                                                                                                           'time',
                                                                                    'product': 'Zendesk Suite',
                                                                                    'relevance': 'Critical',
                                                                                    'url': 'https://www.zendesk.com/pricing/support-suite/',
                                                                                    'why': 'Managing 5+ disconnected '
                                                                                           'tools creates vendor '
                                                                                           'fatigue and renewal chaos. '
                                                                                           'Consolidation reduces '
                                                                                           'costs, simplifies '
                                                                                           'operations, and is a '
                                                                                           'board-level priority.',
                                                                                    'zendesk_name': 'Zendesk Complete '
                                                                                                    'Suite'},
                                                                                {   'addresses_challenge': 'Our '
                                                                                                           'customer '
                                                                                                           'churn is '
                                                                                                           'tied to '
                                                                                                           'support '
                                                                                                           'quality - '
                                                                                                           'we need AI '
                                                                                                           'to scale '
                                                                                                           'without '
                                                                                                           'sacrificing '
                                                                                                           'experience',
                                                                                    'product': 'AI Agents',
                                                                                    'relevance': 'Critical',
                                                                                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                                    'why': 'Churn analysis shows poor '
                                                                                           'support is costing '
                                                                                           'customers. With AI-first '
                                                                                           'strategies on every board '
                                                                                           'agenda, automation '
                                                                                           'directly impacts retention '
                                                                                           'and profitability.',
                                                                                    'zendesk_name': 'Zendesk AI '
                                                                                                    'Agents'}],
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
                                         'pain_points': [   'Managing 50-100 agents across multiple teams/shifts',
                                                            'Complex SLA requirements (different per client/tier)',
                                                            "Legacy tools can't handle current scale"],
                                         'prevalence': '92% of Commercial deals',
                                         'recommended_products': [   {   'addresses_challenge': 'We need to reduce '
                                                                                                'handle time but '
                                                                                                'leadership says we '
                                                                                                "can't compromise on "
                                                                                                'quality - how do we '
                                                                                                'do both?',
                                                                         'product': 'Copilot',
                                                                         'relevance': 'High',
                                                                         'url': 'https://www.zendesk.com/platform/copilot/',
                                                                         'why': 'Cost-per-ticket and CSAT are '
                                                                                'competing priorities. Copilot '
                                                                                'delivers both: 25% faster resolution '
                                                                                'without sacrificing quality or '
                                                                                'customer satisfaction.',
                                                                         'zendesk_name': 'Zendesk AI Copilot'},
                                                                     {   'addresses_challenge': 'Our agents are '
                                                                                                'toggling between '
                                                                                                'seven different '
                                                                                                'systems to resolve '
                                                                                                "one ticket - we're "
                                                                                                'bleeding efficiency',
                                                                         'product': 'Integrations',
                                                                         'relevance': 'Critical',
                                                                         'url': 'https://www.zendesk.com/marketplace/',
                                                                         'why': 'With 62% of Commercial companies '
                                                                                'citing integration needs, connecting '
                                                                                'Salesforce, SAP, and custom systems '
                                                                                'is make-or-break. Agents lose context '
                                                                                'switching between 5+ systems.',
                                                                         'zendesk_name': 'Zendesk Apps & Integrations'},
                                                                     {   'addresses_challenge': 'We need to cut costs '
                                                                                                "but we're drowning in "
                                                                                                'volume - how do we do '
                                                                                                'more with less?',
                                                                         'product': 'AI Agents',
                                                                         'relevance': 'Critical',
                                                                         'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                         'why': 'Ticket volume is outpacing headcount '
                                                                                'growth 3:1. With 42% of Commercial '
                                                                                'facing cost pressure, 40-60% '
                                                                                'automation rates directly impact the '
                                                                                'bottom line.',
                                                                         'zendesk_name': 'Zendesk AI Agents'},
                                                                     {   'addresses_challenge': 'We have different '
                                                                                                'SLAs for different '
                                                                                                'customer tiers and '
                                                                                                "can't route tickets "
                                                                                                "intelligently - we're "
                                                                                                'constantly missing '
                                                                                                'targets',
                                                                         'product': 'Omnichannel Routing',
                                                                         'relevance': 'High',
                                                                         'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                                                                         'why': 'Multi-tier SLAs (platinum, gold, '
                                                                                'silver clients) require intelligent '
                                                                                'routing. Manual assignment misses '
                                                                                'SLAs and creates uneven workload '
                                                                                'distribution.',
                                                                         'zendesk_name': 'Zendesk Omnichannel '
                                                                                         'Routing'}],
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
                                                            'pain_points': [   'Software sprawl - managing 100+ vendor '
                                                                               'relationships',
                                                                               'Shadow IT spending not going through '
                                                                               'procurement',
                                                                               'Unfavorable contract terms inherited '
                                                                               'from previous deals'],
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
                                           'pain_points': [   'Security audits finding vulnerabilities in old tools',
                                                              'Integration sprawl - too many point-to-point '
                                                              'connections',
                                                              'Compliance requirements (GDPR, HIPAA, SOC 2, ISO)'],
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
                                               'pain_points': [   "Manual WFM in spreadsheets - can't forecast "
                                                                  'accurately',
                                                                  'QA team can only review <1% of interactions '
                                                                  'manually',
                                                                  'No real-time visibility into agent performance'],
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
                                                      'pain_points': [   'Juggling multiple communication channels',
                                                                         'No system - using personal email and '
                                                                         'spreadsheets',
                                                                         "Can't find previous conversations with "
                                                                         'customers'],
                                                      'prevalence': '45% of Digital deals',
                                                      'recommended_products': [   {   'addresses_challenge': "I'm "
                                                                                                             'typing '
                                                                                                             'the same '
                                                                                                             'answers '
                                                                                                             'over and '
                                                                                                             'over - '
                                                                                                             'there '
                                                                                                             'has to '
                                                                                                             'be a '
                                                                                                             'better '
                                                                                                             'way',
                                                                                      'product': 'Knowledge Base',
                                                                                      'relevance': 'Critical',
                                                                                      'url': 'https://www.zendesk.com/service/help-center/',
                                                                                      'why': 'Answering the same '
                                                                                             'questions 15 times a day '
                                                                                             'steals time from '
                                                                                             'important work. When '
                                                                                             'customers can '
                                                                                             'self-serve, you can '
                                                                                             'focus on what matters.',
                                                                                      'zendesk_name': 'Zendesk Help '
                                                                                                      'Center'},
                                                                                  {   'addresses_challenge': "I'm not "
                                                                                                             'sure how '
                                                                                                             'to '
                                                                                                             'answer '
                                                                                                             'some of '
                                                                                                             'these '
                                                                                                             'questions '
                                                                                                             'and '
                                                                                                             "there's "
                                                                                                             'no one '
                                                                                                             'to ask '
                                                                                                             'for help',
                                                                                      'product': 'Copilot',
                                                                                      'relevance': 'Medium',
                                                                                      'url': 'https://www.zendesk.com/platform/copilot/',
                                                                                      'why': "When you're the only "
                                                                                             'support person, you '
                                                                                             "don't have anyone to ask "
                                                                                             'for help. Copilot is '
                                                                                             'like having an '
                                                                                             'experienced teammate '
                                                                                             'suggesting answers.',
                                                                                      'zendesk_name': 'Zendesk AI '
                                                                                                      'Copilot'},
                                                                                  {   'addresses_challenge': "I'm "
                                                                                                             'constantly '
                                                                                                             'switching '
                                                                                                             'between '
                                                                                                             'email, '
                                                                                                             'WhatsApp, '
                                                                                                             'Facebook '
                                                                                                             '- I '
                                                                                                             "can't "
                                                                                                             'keep up '
                                                                                                             'with all '
                                                                                                             'these '
                                                                                                             'tabs',
                                                                                      'product': 'Messaging',
                                                                                      'relevance': 'Critical',
                                                                                      'url': 'https://www.zendesk.com/service/messaging/',
                                                                                      'why': 'Switching between 4+ '
                                                                                             'apps to check messages '
                                                                                             'is exhausting and you '
                                                                                             'miss things. One inbox '
                                                                                             'means nothing falls '
                                                                                             'through the cracks.',
                                                                                      'zendesk_name': 'Zendesk '
                                                                                                      'Messaging'},
                                                                                  {   'addresses_challenge': "I'm just "
                                                                                                             'copy-pasting '
                                                                                                             'the same '
                                                                                                             'answers '
                                                                                                             'all day '
                                                                                                             '- it '
                                                                                                             'feels '
                                                                                                             'like '
                                                                                                             'robot '
                                                                                                             'work',
                                                                                      'product': 'AI Agents',
                                                                                      'relevance': 'High',
                                                                                      'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                                      'why': 'Copy-pasting canned '
                                                                                             "responses isn't "
                                                                                             'sustainable. Automation '
                                                                                             'handles the repetitive '
                                                                                             'stuff so you can spend '
                                                                                             'time on customers who '
                                                                                             'actually need help.',
                                                                                      'zendesk_name': 'Zendesk AI '
                                                                                                      'Agents'}],
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
                                        'challenges_from_gong': [   'Price sensitivity - need startup/small business '
                                                                    'pricing',
                                                                    'Self-service implementation required - no IT '
                                                                    'department',
                                                                    'Evaluating against Zoho Desk, HubSpot Service '
                                                                    'Hub, Freshdesk'],
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
                                                          '"I\'m already using Zoho Desk - why switch?"',
                                                          '"Looks complicated - don\'t have time to learn"'],
                                        'pain_points': [   'Wearing too many hats - no time to learn complex tools',
                                                           'Budget constraints - need maximum value at minimum cost',
                                                           'No dedicated support staff - everyone does support'],
                                        'prevalence': '88% of Digital deals',
                                        'recommended_products': [   {   'addresses_challenge': 'I keep answering "how '
                                                                                               'do I reset my '
                                                                                               'password" all day - '
                                                                                               'customers should be '
                                                                                               'able to figure this '
                                                                                               'out themselves',
                                                                        'product': 'Knowledge Base',
                                                                        'relevance': 'High',
                                                                        'url': 'https://www.zendesk.com/service/help-center/',
                                                                        'why': "When you're answering the same "
                                                                               "questions 20 times a day, you're "
                                                                               'losing time on growth activities. '
                                                                               'Self-service frees you from repetitive '
                                                                               'work.',
                                                                        'zendesk_name': 'Zendesk Help Center'},
                                                                    {   'addresses_challenge': 'My customers want to '
                                                                                               'message me on WhatsApp '
                                                                                               'and Instagram, not '
                                                                                               "email - I'm missing "
                                                                                               'inquiries',
                                                                        'product': 'Messaging',
                                                                        'relevance': 'Critical',
                                                                        'url': 'https://www.zendesk.com/service/messaging/',
                                                                        'why': 'Customers expect instant responses on '
                                                                               'WhatsApp and social. With 45% of '
                                                                               'Digital companies prioritizing '
                                                                               "messaging, it's where customers are "
                                                                               'and you need to be there.',
                                                                        'zendesk_name': 'Zendesk Messaging'},
                                                                    {   'addresses_challenge': 'I need to connect to '
                                                                                               "my tools but I don't "
                                                                                               'have an IT person - it '
                                                                                               'needs to just work',
                                                                        'product': 'Integrations',
                                                                        'relevance': 'Critical',
                                                                        'url': 'https://www.zendesk.com/marketplace/',
                                                                        'why': 'With 48% of Digital companies citing '
                                                                               'integration needs, connecting Moodle, '
                                                                               'Respond.io, and basic CRMs is '
                                                                               'critical. No IT team means pre-built '
                                                                               'connectors are essential.',
                                                                        'zendesk_name': 'Zendesk Apps & Integrations'},
                                                                    {   'addresses_challenge': "I can't afford to hire "
                                                                                               'someone but customers '
                                                                                               'need answers at '
                                                                                               'midnight - what do I '
                                                                                               'do?',
                                                                        'product': 'AI Agents',
                                                                        'relevance': 'High',
                                                                        'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                        'why': 'With 44% of Digital facing cost '
                                                                               "pressure, hiring isn't an option. AI "
                                                                               'lets you scale support without payroll '
                                                                               'increases - answering 24/7 for less '
                                                                               'than a part-timer.',
                                                                        'zendesk_name': 'Zendesk AI Agents'}],
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
                                          'challenges_from_gong': [   'Multi-year digital transformation roadmaps',
                                                                      'Contract renewals - optimizing costs while '
                                                                      'improving CX',
                                                                      'Global rollout complexity - 5+ regions, '
                                                                      'compliance requirements'],
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
                                                            '"Our contract is up for renewal - need to cut costs, not '
                                                            'increase them"',
                                                            '"Too risky to migrate 500+ agents"'],
                                          'pain_points': [   "Legacy tools can't scale - platform limitations at 500+ "
                                                             'agents',
                                                             'CX data siloed across systems - no unified customer view',
                                                             'Board pressure for efficiency - "do more with less"'],
                                          'prevalence': '95% of Enterprise deals',
                                          'recommended_products': [   {   'addresses_challenge': 'The board keeps '
                                                                                                 'asking what our CX '
                                                                                                 'investment is '
                                                                                                 'delivering - I need '
                                                                                                 'data that shows '
                                                                                                 'impact on revenue '
                                                                                                 'and retention',
                                                                          'product': 'Analytics',
                                                                          'relevance': 'High',
                                                                          'url': 'https://www.zendesk.com/service/analytics/',
                                                                          'why': 'Quarterly board meetings demand hard '
                                                                                 'numbers on CX ROI. Without unified '
                                                                                 'analytics across regions and brands, '
                                                                                 "you're presenting gut feelings, not "
                                                                                 'data.',
                                                                          'zendesk_name': 'Zendesk Explore'},
                                                                      {   'addresses_challenge': 'We need to support '
                                                                                                 'customers in 20 '
                                                                                                 'languages across '
                                                                                                 'every time zone - '
                                                                                                 'our current tools '
                                                                                                 "can't scale globally",
                                                                          'product': 'Contact Center',
                                                                          'relevance': 'High',
                                                                          'url': 'https://www.zendesk.com/service/contact-center/',
                                                                          'why': 'Supporting 20+ languages across 8 '
                                                                                 'time zones requires enterprise-grade '
                                                                                 "infrastructure. 99.99% uptime isn't "
                                                                                 'optional when downtime costs '
                                                                                 'millions.',
                                                                          'zendesk_name': 'Zendesk Contact Center'},
                                                                      {   'addresses_challenge': 'We have SAP in EMEA, '
                                                                                                 'Oracle in APAC, and '
                                                                                                 'ServiceNow in the US '
                                                                                                 "- we can't operate "
                                                                                                 'in silos anymore',
                                                                          'product': 'Integrations',
                                                                          'relevance': 'Critical',
                                                                          'url': 'https://www.zendesk.com/marketplace/',
                                                                          'why': 'Global transformation depends on '
                                                                                 'connecting SAP, ServiceNow, and '
                                                                                 'regional systems across 5+ '
                                                                                 'countries. With 40% of Enterprise '
                                                                                 'citing integration complexity, this '
                                                                                 'is the foundation.',
                                                                          'zendesk_name': 'Zendesk Enterprise '
                                                                                          'Integration Platform'},
                                                                      {   'addresses_challenge': 'The board wants to '
                                                                                                 'know why we need 500 '
                                                                                                 'agents - prove we '
                                                                                                 'can reduce '
                                                                                                 'cost-to-serve '
                                                                                                 'without hurting NPS',
                                                                          'product': 'AI Agents',
                                                                          'relevance': 'Critical',
                                                                          'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                          'why': 'Board wants proof that CX '
                                                                                 'investments deliver ROI. With 38% of '
                                                                                 'Enterprise facing cost pressure, '
                                                                                 'automation at Fortune 500 scale '
                                                                                 '(100K+ daily conversations) is table '
                                                                                 'stakes.',
                                                                          'zendesk_name': 'Zendesk AI Agents'}],
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
                                                                       'SAP/Oracle/ServiceNow/X plan environment?"',
                                                                       '"What\'s the total cost of implementation and '
                                                                       'maintenance?"'],
                                                     'pain_points': [   'Shadow IT - departments buying SaaS without '
                                                                        'IT approval',
                                                                        'Integration complexity - 200+ enterprise '
                                                                        'systems',
                                                                        'Security and compliance risks at scale'],
                                                     'prevalence': '85% of Enterprise deals',
                                                     'recommended_products': [   {   'addresses_challenge': 'Our '
                                                                                                            'compliance '
                                                                                                            'team '
                                                                                                            "won't "
                                                                                                            'approve '
                                                                                                            'any tool '
                                                                                                            'that '
                                                                                                            "isn't SOC "
                                                                                                            '2 and ISO '
                                                                                                            'certified '
                                                                                                            'with '
                                                                                                            'regional '
                                                                                                            'data '
                                                                                                            'residency',
                                                                                     'product': 'Enterprise Security',
                                                                                     'relevance': 'Critical',
                                                                                     'url': 'https://www.zendesk.com/product/security/',
                                                                                     'why': 'Failed audits block '
                                                                                            'enterprise deals and '
                                                                                            'expose regulatory risk. '
                                                                                            'With GDPR, HIPAA, and '
                                                                                            'FedRAMP requirements, '
                                                                                            "compliance isn't "
                                                                                            "optional—it's the price "
                                                                                            'of entry.',
                                                                                     'zendesk_name': 'Zendesk '
                                                                                                     'Enterprise '
                                                                                                     'Security & '
                                                                                                     'Compliance'},
                                                                                 {   'addresses_challenge': 'We need '
                                                                                                            'to '
                                                                                                            'integrate '
                                                                                                            'with '
                                                                                                            'systems '
                                                                                                            'that '
                                                                                                            "don't "
                                                                                                            'have '
                                                                                                            'out-of-box '
                                                                                                            'connectors '
                                                                                                            '- show me '
                                                                                                            'your API '
                                                                                                            'documentation',
                                                                                     'product': 'Enterprise APIs',
                                                                                     'relevance': 'Critical',
                                                                                     'url': 'https://developer.zendesk.com/api-reference/',
                                                                                     'why': 'Enterprise architecture '
                                                                                            'depends on connecting '
                                                                                            'SAP, Oracle, and '
                                                                                            'ServiceNow. With 40% of '
                                                                                            'Enterprise citing '
                                                                                            'integration needs, robust '
                                                                                            'APIs and pre-built '
                                                                                            'connectors are '
                                                                                            'non-negotiable.',
                                                                                     'zendesk_name': 'Zendesk '
                                                                                                     'Enterprise APIs'},
                                                                                 {   'addresses_challenge': 'We tried '
                                                                                                            'to do our '
                                                                                                            'last '
                                                                                                            'implementation '
                                                                                                            'ourselves '
                                                                                                            'and it '
                                                                                                            'took two '
                                                                                                            'years - '
                                                                                                            'we need '
                                                                                                            'experts '
                                                                                                            'this time',
                                                                                     'product': 'Professional Services',
                                                                                     'relevance': 'High',
                                                                                     'url': 'https://www.zendesk.com/services/',
                                                                                     'why': 'Global rollouts spanning '
                                                                                            "12-18 months can't rely "
                                                                                            'on self-service. '
                                                                                            'Dedicated solutions '
                                                                                            'architects prevent costly '
                                                                                            'mistakes and accelerate '
                                                                                            'time-to-value.',
                                                                                     'zendesk_name': 'Zendesk '
                                                                                                     'Professional '
                                                                                                     'Services'}],
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
                                                      'pain_points': [   'Workforce management complexity - scheduling '
                                                                         '100s across time zones',
                                                                         'Process inconsistency across regions',
                                                                         "Quality assurance at scale - can't review "
                                                                         'enough interactions'],
                                                      'prevalence': '72% of Enterprise deals',
                                                      'recommended_products': [   {   'addresses_challenge': "We're "
                                                                                                             'managing '
                                                                                                             'global '
                                                                                                             'shifts '
                                                                                                             'in '
                                                                                                             'spreadsheets '
                                                                                                             '- we '
                                                                                                             'need WFM '
                                                                                                             'that '
                                                                                                             'integrates '
                                                                                                             'with '
                                                                                                             'Nice and '
                                                                                                             'handles '
                                                                                                             '20 '
                                                                                                             'languages',
                                                                                      'product': 'Contact Center',
                                                                                      'relevance': 'Critical',
                                                                                      'url': 'https://www.zendesk.com/service/contact-center/',
                                                                                      'why': 'Scheduling 500 agents '
                                                                                             'across 8 time zones '
                                                                                             'without WFM integration '
                                                                                             'is chaos. With 21% of '
                                                                                             'Enterprise prioritizing '
                                                                                             'contact center, '
                                                                                             'enterprise-grade '
                                                                                             'infrastructure is '
                                                                                             'essential.',
                                                                                      'zendesk_name': 'Zendesk Contact '
                                                                                                      'Center'},
                                                                                  {   'addresses_challenge': "We're "
                                                                                                             'missing '
                                                                                                             'SLAs '
                                                                                                             'because '
                                                                                                             'tickets '
                                                                                                             'sit in '
                                                                                                             'queues '
                                                                                                             'while '
                                                                                                             'agents '
                                                                                                             'are idle '
                                                                                                             'in other '
                                                                                                             'queues - '
                                                                                                             'routing '
                                                                                                             'is '
                                                                                                             'broken',
                                                                                      'product': 'Omnichannel Routing',
                                                                                      'relevance': 'Critical',
                                                                                      'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                                                                                      'why': 'Missing 95% SLA targets '
                                                                                             'damages client '
                                                                                             'relationships and costs '
                                                                                             'penalties. Intelligent '
                                                                                             'routing with capacity '
                                                                                             'management is the only '
                                                                                             'way to maintain '
                                                                                             'enterprise-level '
                                                                                             'performance.',
                                                                                      'zendesk_name': 'Zendesk '
                                                                                                      'Omnichannel '
                                                                                                      'Routing'},
                                                                                  {   'addresses_challenge': 'Our QA '
                                                                                                             'team can '
                                                                                                             'only '
                                                                                                             'review '
                                                                                                             '1% of '
                                                                                                             'calls - '
                                                                                                             'we have '
                                                                                                             'no idea '
                                                                                                             'what '
                                                                                                             'quality '
                                                                                                             'looks '
                                                                                                             'like in '
                                                                                                             'Manila '
                                                                                                             'or '
                                                                                                             'Warsaw',
                                                                                      'product': 'QA & Analytics',
                                                                                      'relevance': 'High',
                                                                                      'url': 'https://www.zendesk.com/service/qa/',
                                                                                      'why': 'Manual QA sampling '
                                                                                             'catches less than 1% of '
                                                                                             'problems. When process '
                                                                                             'gaps hide across 8 sites '
                                                                                             'and 20 languages, '
                                                                                             'AI-powered 100% review '
                                                                                             'is the only way to '
                                                                                             'identify issues.',
                                                                                      'zendesk_name': 'Zendesk QA & '
                                                                                                      'Explore'},
                                                                                  {   'addresses_challenge': 'Finance '
                                                                                                             'wants us '
                                                                                                             'to cut '
                                                                                                             'cost-per-ticket '
                                                                                                             'by 30% '
                                                                                                             'but we '
                                                                                                             "can't "
                                                                                                             'reduce '
                                                                                                             'quality '
                                                                                                             '- how do '
                                                                                                             'we do '
                                                                                                             'both?',
                                                                                      'product': 'AI Agents',
                                                                                      'relevance': 'High',
                                                                                      'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                                      'why': 'Leadership wants to '
                                                                                             'reduce cost-per-ticket '
                                                                                             'by 30% without hurting '
                                                                                             'CSAT. Automation at '
                                                                                             'scale is the only path '
                                                                                             'to that math.',
                                                                                      'zendesk_name': 'Zendesk AI '
                                                                                                      'Agents'}],
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
                                             'pain_points': [   'Support costs rising faster than revenue',
                                                                'Customer complaints about slow service impacting '
                                                                'retention',
                                                                'Hiring freeze but ticket volume up 30-40%'],
                                             'prevalence': '68% of SMB deals',
                                             'recommended_products': [   {   'addresses_challenge': "I can't tell you "
                                                                                                    'if our support '
                                                                                                    'investment is '
                                                                                                    'paying off - '
                                                                                                    "we're flying "
                                                                                                    'blind',
                                                                             'product': 'Analytics',
                                                                             'relevance': 'High',
                                                                             'url': 'https://www.zendesk.com/service/analytics/',
                                                                             'why': "Without clear ROI metrics, it's "
                                                                                    'impossible to justify support '
                                                                                    'investments to the board. '
                                                                                    "Real-time dashboards prove what's "
                                                                                    "working and what's waste.",
                                                                             'zendesk_name': 'Zendesk Explore'},
                                                                         {   'addresses_challenge': "We're spending "
                                                                                                    'money on people '
                                                                                                    'doing manual work '
                                                                                                    'that technology '
                                                                                                    'should handle',
                                                                             'product': 'Copilot',
                                                                             'relevance': 'Medium',
                                                                             'url': 'https://www.zendesk.com/platform/copilot/',
                                                                             'why': 'Agent productivity directly '
                                                                                    'impacts cost per ticket. When '
                                                                                    'teams lack automation, you pay '
                                                                                    'for manual work that should be '
                                                                                    'automated.',
                                                                             'zendesk_name': 'Zendesk AI Copilot'},
                                                                         {   'addresses_challenge': 'Our support costs '
                                                                                                    'are eating into '
                                                                                                    'margins - we '
                                                                                                    "can't keep hiring "
                                                                                                    'agents every time '
                                                                                                    'volume grows',
                                                                             'product': 'Knowledge Base',
                                                                             'relevance': 'High',
                                                                             'url': 'https://www.zendesk.com/service/help-center/',
                                                                             'why': 'Every self-served customer is one '
                                                                                    'less agent needed. With cost per '
                                                                                    'ticket rising, self-service '
                                                                                    'directly impacts profitability '
                                                                                    'and lets you scale efficiently.',
                                                                             'zendesk_name': 'Zendesk Help Center'},
                                                                         {   'addresses_challenge': 'We need to cut '
                                                                                                    'costs - support '
                                                                                                    'headcount is '
                                                                                                    'growing faster '
                                                                                                    'than revenue',
                                                                             'product': 'AI Agents',
                                                                             'relevance': 'Critical',
                                                                             'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                             'why': 'Board wants to see growth without '
                                                                                    'proportional cost increases. With '
                                                                                    '47% of SMB facing cost pressure, '
                                                                                    'automation directly impacts the '
                                                                                    'bottom line and customer '
                                                                                    'retention.',
                                                                             'zendesk_name': 'Zendesk AI Agents'}],
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
                                  'pain_points': [   'Agents overwhelmed with ticket volume (backlog growing)',
                                                     'Missing SLA targets due to manual routing and slow response '
                                                     'times',
                                                     'Customers calling for simple/repetitive questions that could be '
                                                     'self-served'],
                                  'prevalence': '98% of SMB deals',
                                  'recommended_products': [   {   'addresses_challenge': 'Our agents are drowning in '
                                                                                         'tickets and our best people '
                                                                                         'are burning out from '
                                                                                         'repetitive work',
                                                                  'product': 'Copilot',
                                                                  'relevance': 'High',
                                                                  'url': 'https://www.zendesk.com/platform/copilot/',
                                                                  'why': 'Agent burnout and turnover hurt consistency. '
                                                                         'When SLA targets are missed and handle time '
                                                                         'is too long, Copilot helps agents resolve '
                                                                         'faster without quality drops.',
                                                                  'zendesk_name': 'Zendesk AI Copilot'},
                                                              {   'addresses_challenge': 'Customers are calling us for '
                                                                                         'password resets and order '
                                                                                         'status - things they should '
                                                                                         'be able to do themselves',
                                                                  'product': 'Knowledge Base',
                                                                  'relevance': 'High',
                                                                  'url': 'https://www.zendesk.com/service/help-center/',
                                                                  'why': 'When simple questions eat up 40% of ticket '
                                                                         'volume, self-service becomes '
                                                                         'mission-critical. Especially with cost '
                                                                         'pressure - every deflected ticket saves '
                                                                         'money.',
                                                                  'zendesk_name': 'Zendesk Help Center'},
                                                              {   'addresses_challenge': "We can't keep switching "
                                                                                         'between five different '
                                                                                         'systems just to answer one '
                                                                                         'customer question',
                                                                  'product': 'Integrations',
                                                                  'relevance': 'Critical',
                                                                  'url': 'https://www.zendesk.com/marketplace/',
                                                                  'why': 'With agents juggling 3+ tools to help one '
                                                                         'customer, context is lost and response times '
                                                                         'suffer. Integration gaps cause 43% of SMB CX '
                                                                         'leaders to delay purchases.',
                                                                  'zendesk_name': 'Zendesk Apps & Integrations'},
                                                              {   'addresses_challenge': 'We need to cut costs but our '
                                                                                         'support volume keeps growing '
                                                                                         "- we can't afford to keep "
                                                                                         'hiring',
                                                                  'product': 'AI Agents',
                                                                  'relevance': 'Critical',
                                                                  'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                  'why': 'Ticket backlogs are growing faster than '
                                                                         'hiring. With cost pressure affecting 47% of '
                                                                         'SMB buyers, automation is the only way to '
                                                                         'scale without adding headcount.',
                                                                  'zendesk_name': 'Zendesk AI Agents'}],
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
                                                     'pain_points': [   'Support costs growing faster than revenue',
                                                                        'Software sprawl - too many subscriptions',
                                                                        'Getting nickel-and-dimed with add-on fees'],
                                                     'prevalence': '42% of SMB deals',
                                                     'recommended_products': [   {   'addresses_challenge': "I can't "
                                                                                                            'tell if '
                                                                                                            'our '
                                                                                                            'support '
                                                                                                            'investment '
                                                                                                            'is worth '
                                                                                                            'it - show '
                                                                                                            'me the '
                                                                                                            'ROI in '
                                                                                                            'dollars',
                                                                                     'product': 'Analytics',
                                                                                     'relevance': 'Medium',
                                                                                     'url': 'https://www.zendesk.com/service/analytics/',
                                                                                     'why': 'Without hard metrics, '
                                                                                            'support spend is a black '
                                                                                            'box. Real-time ROI '
                                                                                            'tracking (cost per '
                                                                                            'ticket, deflection rates) '
                                                                                            'justifies budget and '
                                                                                            'identifies waste.',
                                                                                     'zendesk_name': 'Zendesk Explore'},
                                                                                 {   'addresses_challenge': 'We have '
                                                                                                            'too many '
                                                                                                            'software '
                                                                                                            'subscriptions '
                                                                                                            '- I need '
                                                                                                            'to '
                                                                                                            'consolidate '
                                                                                                            'vendors '
                                                                                                            'and '
                                                                                                            'reduce '
                                                                                                            'spend',
                                                                                     'product': 'Zendesk Suite',
                                                                                     'relevance': 'High',
                                                                                     'url': 'https://www.zendesk.com/pricing/support-suite/',
                                                                                     'why': 'Managing 5+ separate '
                                                                                            'vendor contracts '
                                                                                            'increases procurement '
                                                                                            'overhead and renewal '
                                                                                            'chaos. Vendor '
                                                                                            'consolidation directly '
                                                                                            'reduces costs and '
                                                                                            'simplifies budgeting.',
                                                                                     'zendesk_name': 'Zendesk Suite'},
                                                                                 {   'addresses_challenge': 'Our '
                                                                                                            'support '
                                                                                                            'budget is '
                                                                                                            'growing '
                                                                                                            'faster '
                                                                                                            'than '
                                                                                                            'revenue - '
                                                                                                            'we need '
                                                                                                            'ROI or '
                                                                                                            "we're "
                                                                                                            'cutting '
                                                                                                            'headcount',
                                                                                     'product': 'AI Agents',
                                                                                     'relevance': 'High',
                                                                                     'url': 'https://www.zendesk.com/platform/ai-agents/',
                                                                                     'why': 'Support costs growing '
                                                                                            'faster than revenue is '
                                                                                            'unsustainable. With 47% '
                                                                                            'of SMB facing cost '
                                                                                            'pressure, automation '
                                                                                            'offers clear payback: one '
                                                                                            'agent salary funds 10+ '
                                                                                            'licenses.',
                                                                                     'zendesk_name': 'Zendesk AI '
                                                                                                     'Agents'}],
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
                                    'pain_points': [   'Too many support requests for password resets and access '
                                                       'issues',
                                                       'Security audits flagging old/insecure tools',
                                                       'Integration sprawl - too many point solutions to manage'],
                                    'prevalence': '30% of SMB deals',
                                    'recommended_products': [   {   'addresses_challenge': 'We failed our last '
                                                                                           'security audit because our '
                                                                                           "support tools don't have "
                                                                                           'proper access controls',
                                                                    'product': 'SSO & Security',
                                                                    'relevance': 'Critical',
                                                                    'url': 'https://www.zendesk.com/product/security/',
                                                                    'why': 'Security audits are blocking deals and '
                                                                           'exposing risk. With compliance '
                                                                           'requirements tightening, SOC 2 and SAML '
                                                                           'SSO are table stakes to avoid security '
                                                                           'incidents.',
                                                                    'zendesk_name': 'Zendesk Enterprise Security'},
                                                                {   'addresses_challenge': "We can't connect our "
                                                                                           'systems - we have seven '
                                                                                           "different tools that don't "
                                                                                           'talk to each other',
                                                                    'product': 'Integrations & APIs',
                                                                    'relevance': 'Critical',
                                                                    'url': 'https://www.zendesk.com/marketplace/',
                                                                    'why': 'Managing 5+ disconnected point solutions '
                                                                           'creates security gaps and maintenance '
                                                                           'overhead. Integration sprawl is a top '
                                                                           'concern for 43% of SMB IT teams.',
                                                                    'zendesk_name': 'Zendesk APIs & Marketplace'},
                                                                {   'addresses_challenge': 'I have no idea who has '
                                                                                           'access to what customer '
                                                                                           "data - it's a compliance "
                                                                                           'nightmare',
                                                                    'product': 'Admin Tools',
                                                                    'relevance': 'High',
                                                                    'url': 'https://www.zendesk.com/',
                                                                    'why': 'Without centralized user management, '
                                                                           'offboarding is slow and risky. Role-based '
                                                                           'access and audit logs are essential for '
                                                                           'compliance and preventing data breaches.',
                                                                    'zendesk_name': 'Zendesk Admin Center'}],
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
                                        'pain_points': [   'Manual scheduling in spreadsheets',
                                                           "Can't forecast volume accurately - over/understaffed",
                                                           'QA done manually on <5% of interactions'],
                                        'prevalence': '22% of SMB deals',
                                        'recommended_products': [   {   'addresses_challenge': "I can't tell you why "
                                                                                               'tickets are piling up '
                                                                                               'or which agents need '
                                                                                               'help - we have no '
                                                                                               'real-time visibility',
                                                                        'product': 'Analytics',
                                                                        'relevance': 'Critical',
                                                                        'url': 'https://www.zendesk.com/service/analytics/',
                                                                        'why': 'Flying blind on agent performance and '
                                                                               'volume trends means constant '
                                                                               'firefighting. Real-time dashboards '
                                                                               'turn reactive ops into proactive '
                                                                               'optimization.',
                                                                        'zendesk_name': 'Zendesk Explore'},
                                                                    {   'addresses_challenge': 'We only QA 5% of '
                                                                                               'tickets - we have no '
                                                                                               "idea what's actually "
                                                                                               'happening in most '
                                                                                               'customer interactions',
                                                                        'product': 'QA & Coaching',
                                                                        'relevance': 'Critical',
                                                                        'url': 'https://www.zendesk.com/service/qa/',
                                                                        'why': 'Manual QA sampling misses 95% of '
                                                                               'interactions and coaching is reactive. '
                                                                               'When process gaps hide in blind spots, '
                                                                               'quality suffers and problems escalate.',
                                                                        'zendesk_name': 'Zendesk QA'},
                                                                    {   'addresses_challenge': 'Our forecasting is '
                                                                                               "guesswork - we're "
                                                                                               'either overstaffed '
                                                                                               'wasting money or '
                                                                                               'understaffed missing '
                                                                                               'SLAs',
                                                                        'product': 'Omnichannel Routing',
                                                                        'relevance': 'High',
                                                                        'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                                                                        'why': 'Manual routing creates uneven workload '
                                                                               'distribution and long wait times. '
                                                                               'Intelligent routing optimizes capacity '
                                                                               'and improves SLA performance.',
                                                                        'zendesk_name': 'Zendesk Omnichannel Routing'}],
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
