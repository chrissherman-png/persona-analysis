"""
Generate detailed persona profiles for SMB and Commercial segments
Based on real Gong data analysis
"""

personas = {
    'SMB': {
        'CX Champion': {
            'job_titles': [
                'VP Customer Service',
                'Director of Customer Support',
                'Head of Customer Experience',
                'Customer Service Manager',
                'Support Manager'
            ],
            'reports_to': 'COO or CEO',
            'team_size': '5-25 agents',
            'prevalence': '98% of SMB deals',
            'role_in_deal': 'Primary Champion & Decision Driver',

            'goals': [
                'Reduce agent handle time and improve productivity',
                'Meet or exceed SLA targets (1-4 hour first response)',
                'Improve CSAT/NPS scores',
                'Scale support without adding headcount',
                'Implement self-service to deflect simple tickets',
                'Reduce customer churn by improving support experience'
            ],

            'pain_points': [
                'Agents overwhelmed with ticket volume (backlog growing)',
                'Missing SLA targets due to manual routing and slow response times',
                'Customers calling for simple/repetitive questions that could be self-served',
                'No real-time visibility into team performance',
                'Manual reporting in Excel - hours wasted each week',
                'High agent turnover due to repetitive work and burnout'
            ],

            'challenges_from_gong': [
                'Integration gaps - switching between Zendesk, CRM, and 3+ other tools',
                'Incomplete help center - lacking self-service articles',
                'No AI/automation - manually routing and responding to every ticket',
                'Can\'t see what\'s happening in real-time - blind to bottlenecks',
                'Agent burnout from repetitive work'
            ],

            'evaluation_criteria': [
                '**#1 Priority:** Ease of implementation & time to value (want live in 2-4 weeks)',
                'Simple, intuitive interface agents can learn in days',
                'Out-of-box integrations with existing tools (Salesforce, Slack)',
                'Clear ROI story - ticket deflection, faster resolution times',
                'Responsive support during onboarding'
            ],

            'objections': [
                '"We don\'t have time for a long implementation"',
                '"Our agents are already learning too many new tools"',
                '"We tried AI before and it gave wrong answers to customers"',
                '"Not sure if we can afford this right now"',
                '"What if the AI makes mistakes with customer data?"'
            ],

            'key_messages': [
                'Live in 2 weeks with minimal IT involvement',
                'Agents love it - 4.5★ ease of use rating',
                'Agent productivity up 30% in first 90 days (via automation)',
                'Self-service deflects 30-40% of tickets automatically',
                'Real-time dashboards replace Excel reporting',
                '95% AI accuracy rate with built-in safeguards and human oversight'
            ],

            'content_preferences': [
                'Customer testimonials from similar-sized companies',
                'Quick demo videos (5-10 min)',
                'ROI calculators',
                'Implementation timelines',
                'Free trial or POC to test with team'
            ],

            'success_metrics': [
                'First response time (target: <1 hour)',
                'CSAT score',
                'Ticket volume & deflection rate',
                'Agent productivity (tickets per agent per day)',
                'Time to resolution'
            ],

            'buying_behavior': {
                'decision_speed': '45-60 days',
                'committee_size': '3-4 people (CX Champion, C-Suite, Finance, sometimes IT)',
                'authority_level': 'High - can often drive decision with C-Suite approval',
                'prefers': 'Fast-moving pilots over long enterprise sales cycles'
            },

            'recommended_products': [
                {
                    'product': 'Integrations',
                    'zendesk_name': 'Zendesk Apps & Integrations',
                    'url': 'https://www.zendesk.com/marketplace/',
                    'relevance': 'Critical',
                    'why': 'With agents juggling 3+ tools to help one customer, context is lost and response times suffer. Integration gaps cause 43% of SMB CX leaders to delay purchases.',
                    'addresses_challenge': 'We can\'t keep switching between five different systems just to answer one customer question'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'Critical',
                    'why': 'Ticket backlogs are growing faster than hiring. With cost pressure affecting 47% of SMB buyers, automation is the only way to scale without adding headcount.',
                    'addresses_challenge': 'We need to cut costs but our support volume keeps growing - we can\'t afford to keep hiring'
                },
                {
                    'product': 'Copilot',
                    'zendesk_name': 'Zendesk AI Copilot',
                    'url': 'https://www.zendesk.com/platform/copilot/',
                    'relevance': 'High',
                    'why': 'Agent burnout and turnover hurt consistency. When SLA targets are missed and handle time is too long, Copilot helps agents resolve faster without quality drops.',
                    'addresses_challenge': 'Our agents are drowning in tickets and our best people are burning out from repetitive work'
                },
                {
                    'product': 'Knowledge Base',
                    'zendesk_name': 'Zendesk Help Center',
                    'url': 'https://www.zendesk.com/service/help-center/',
                    'relevance': 'High',
                    'why': 'When simple questions eat up 40% of ticket volume, self-service becomes mission-critical. Especially with cost pressure - every deflected ticket saves money.',
                    'addresses_challenge': 'Customers are calling us for password resets and order status - things they should be able to do themselves'
                }
            ]
        },

        'C-Suite Decision Maker': {
            'job_titles': [
                'CEO',
                'COO',
                'President',
                'Founder'
            ],
            'reports_to': 'Board or self (Owner)',
            'team_size': 'Entire company (50-249 employees)',
            'prevalence': '68% of SMB deals',
            'role_in_deal': 'Budget Holder & Final Approver',

            'goals': [
                'Enable company growth without proportional headcount increases',
                'Improve customer satisfaction and retention',
                'Operational efficiency - do more with less',
                'Make data-driven decisions about support investments',
                'Keep costs predictable and manageable'
            ],

            'pain_points': [
                'Support costs rising faster than revenue',
                'Customer complaints about slow service impacting retention',
                'Hiring freeze but ticket volume up 30-40%',
                'Support team using outdated tools - slowing everything down',
                'No clear visibility into support ROI'
            ],

            'challenges_from_gong': [
                'Scaling challenges - can\'t keep hiring agents to handle volume',
                'Lack of automation - too much manual work',
                'Poor customer experience hurting brand reputation',
                'No real-time business intelligence on support operations',
                'Tech debt - using 5-year-old support tool'
            ],

            'evaluation_criteria': [
                '**#1 Priority:** Clear ROI - will this help us grow without adding headcount?',
                'Total cost of ownership (not just license cost)',
                'Implementation risk - can we do this without disrupting business?',
                'Scalability - will this grow with us to 500 employees?',
                'Vendor stability - is this company going to be around?'
            ],

            'objections': [
                '"How do I know this will actually improve our metrics?"',
                '"What if implementation goes wrong and our support grinds to a halt?"',
                '"Can we really afford this in this economy?"',
                '"We just invested in [other tool] last year"'
            ],

            'key_messages': [
                'Grow support capacity 2x without doubling headcount (AI + automation)',
                'Predictable pricing - no surprise costs as you scale',
                'Fast implementation = minimal business disruption',
                'Proven ROI: customers see 30% productivity gains in 90 days',
                'Modern platform - won\'t need to replace again in 3 years'
            ],

            'content_preferences': [
                'Executive briefings (15 min max)',
                'ROI case studies from similar companies',
                'Analyst reports (Gartner, Forrester)',
                'Board-ready business case templates',
                'CFO-approved pricing models'
            ],

            'success_metrics': [
                'Cost per ticket',
                'Support cost as % of revenue',
                'Customer retention rate',
                'NPS',
                'Agent headcount vs. ticket volume ratio'
            ],

            'buying_behavior': {
                'decision_speed': 'Fast (30-60 days once engaged)',
                'committee_size': '2-3 (CEO, CX Champion, sometimes CFO)',
                'authority_level': 'Ultimate - final say on budget',
                'prefers': 'Concise business case, minimal meetings'
            },

            'recommended_products': [
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'Critical',
                    'why': 'Board wants to see growth without proportional cost increases. With 47% of SMB facing cost pressure, automation directly impacts the bottom line and customer retention.',
                    'addresses_challenge': 'We need to cut costs - support headcount is growing faster than revenue'
                },
                {
                    'product': 'Analytics',
                    'zendesk_name': 'Zendesk Explore',
                    'url': 'https://www.zendesk.com/service/analytics/',
                    'relevance': 'High',
                    'why': 'Without clear ROI metrics, it\'s impossible to justify support investments to the board. Real-time dashboards prove what\'s working and what\'s waste.',
                    'addresses_challenge': 'I can\'t tell you if our support investment is paying off - we\'re flying blind'
                },
                {
                    'product': 'Knowledge Base',
                    'zendesk_name': 'Zendesk Help Center',
                    'url': 'https://www.zendesk.com/service/help-center/',
                    'relevance': 'High',
                    'why': 'Every self-served customer is one less agent needed. With cost per ticket rising, self-service directly impacts profitability and lets you scale efficiently.',
                    'addresses_challenge': 'Our support costs are eating into margins - we can\'t keep hiring agents every time volume grows'
                },
                {
                    'product': 'Copilot',
                    'zendesk_name': 'Zendesk AI Copilot',
                    'url': 'https://www.zendesk.com/platform/copilot/',
                    'relevance': 'Medium',
                    'why': 'Agent productivity directly impacts cost per ticket. When teams lack automation, you pay for manual work that should be automated.',
                    'addresses_challenge': 'We\'re spending money on people doing manual work that technology should handle'
                }
            ]
        },

        'IT Influencer': {
            'job_titles': [
                'IT Manager',
                'Head of IT',
                'Director of IT',
                'Systems Administrator'
            ],
            'reports_to': 'COO, CEO, or CTO',
            'team_size': '1-5 IT staff',
            'prevalence': '30% of SMB deals',
            'role_in_deal': 'Advisor & Validator (not blocker)',

            'goals': [
                'Ensure security and compliance (SOC 2, data encryption)',
                'Minimize IT support burden - want tools that "just work"',
                'Protect existing infrastructure investments',
                'Enable integrations without custom development',
                'SSO and user provisioning automation'
            ],

            'pain_points': [
                'Too many support requests for password resets and access issues',
                'Security audits flagging old/insecure tools',
                'Integration sprawl - too many point solutions to manage',
                'Shadow IT - teams buying tools without IT approval',
                'Lack of visibility into who has access to what data'
            ],

            'challenges_from_gong': [
                'Security concerns even in SMB (SOC 2, encryption, SSO)',
                'Integration requirements - need to connect to existing stack',
                'Limited IT resources - can\'t support complex implementations',
                'Data residency and compliance questions',
                'API access for automation'
            ],

            'evaluation_criteria': [
                'Security certifications (SOC 2 Type 2, ISO 27001)',
                'SSO support (SAML, Okta, Azure AD)',
                'API quality and documentation',
                'Pre-built integrations vs. custom development needs',
                'IT support load - how much will this require from our team?'
            ],

            'objections': [
                '"Does this meet our security requirements?"',
                '"How much custom development will we need?"',
                '"What happens if the integration breaks?"',
                '"Can we get this through our security review in time?"'
            ],

            'key_messages': [
                'Enterprise-grade security built in (SOC 2, SSO, encryption)',
                'Zero IT burden - cloud-hosted, auto-updates, 99.9% uptime',
                'Pre-built integrations with 1000+ tools',
                'Robust APIs for custom workflows',
                'Dedicated security documentation for audits'
            ],

            'content_preferences': [
                'Security whitepapers',
                'API documentation',
                'Integration guides',
                'Architecture diagrams',
                'Compliance certifications'
            ],

            'success_metrics': [
                'Security audit pass rate',
                'System uptime',
                'Integration stability',
                'IT support tickets related to the tool',
                'User provisioning time'
            ],

            'buying_behavior': {
                'decision_speed': 'Quick review (1-2 weeks)',
                'committee_size': 'Solo or with CISO',
                'authority_level': 'Advisory - can flag risks but rarely blocks',
                'prefers': 'Technical documentation, sandbox access'
            },

            'recommended_products': [
                {
                    'product': 'SSO & Security',
                    'zendesk_name': 'Zendesk Enterprise Security',
                    'url': 'https://www.zendesk.com/product/security/',
                    'relevance': 'Critical',
                    'why': 'Security audits are blocking deals and exposing risk. With compliance requirements tightening, SOC 2 and SAML SSO are table stakes to avoid security incidents.',
                    'addresses_challenge': 'We failed our last security audit because our support tools don\'t have proper access controls'
                },
                {
                    'product': 'Integrations & APIs',
                    'zendesk_name': 'Zendesk APIs & Marketplace',
                    'url': 'https://www.zendesk.com/marketplace/',
                    'relevance': 'Critical',
                    'why': 'Managing 5+ disconnected point solutions creates security gaps and maintenance overhead. Integration sprawl is a top concern for 43% of SMB IT teams.',
                    'addresses_challenge': 'We can\'t connect our systems - we have seven different tools that don\'t talk to each other'
                },
                {
                    'product': 'Admin Tools',
                    'zendesk_name': 'Zendesk Admin Center',
                    'url': 'https://www.zendesk.com/',
                    'relevance': 'High',
                    'why': 'Without centralized user management, offboarding is slow and risky. Role-based access and audit logs are essential for compliance and preventing data breaches.',
                    'addresses_challenge': 'I have no idea who has access to what customer data - it\'s a compliance nightmare'
                }
            ]
        },

        'Operations Leader': {
            'job_titles': [
                'Operations Manager',
                'Service Delivery Manager',
                'Director of Operations'
            ],
            'reports_to': 'COO or CX Champion',
            'team_size': 'Oversees support ops + WFM',
            'prevalence': '22% of SMB deals',
            'role_in_deal': 'Influencer (when present)',

            'goals': [
                'Optimize agent scheduling and capacity planning',
                'Improve quality assurance and coaching',
                'Reduce operational costs',
                'Better workforce management and forecasting',
                'Identify process improvement opportunities'
            ],

            'pain_points': [
                'Manual scheduling in spreadsheets',
                'Can\'t forecast volume accurately - over/understaffed',
                'QA done manually on <5% of interactions',
                'No visibility into agent performance patterns',
                'Process bottlenecks not visible until too late'
            ],

            'challenges_from_gong': [
                'Workforce management gaps - scheduling, forecasting',
                'Quality assurance limitations - can\'t review at scale',
                'Reporting fragmented across multiple tools',
                'No real-time operational visibility',
                'Process inefficiencies hard to identify'
            ],

            'evaluation_criteria': [
                'WFM capabilities or integrations',
                'QA and coaching tools',
                'Reporting and analytics depth',
                'Real-time operational dashboards',
                'Process automation capabilities'
            ],

            'objections': [
                '"We already have WFM tools - will this integrate?"',
                '"Can this handle our QA workflows?"',
                '"Is the reporting customizable enough?"'
            ],

            'key_messages': [
                'Built-in QA tools to review 100% of interactions (AI-powered)',
                'Integrates with WFM platforms (Calabrio, Verint, etc.)',
                'Real-time operational dashboards',
                'Agent performance analytics and coaching tools',
                'Workflow automation to eliminate manual processes'
            ],

            'content_preferences': [
                'WFM integration guides',
                'QA best practices',
                'Operational metrics benchmarks',
                'Process optimization case studies'
            ],

            'success_metrics': [
                'Schedule adherence',
                'Occupancy rate',
                'QA score trends',
                'Process cycle time',
                'Operational cost per ticket'
            ],

            'buying_behavior': {
                'decision_speed': 'N/A - not decision maker',
                'committee_size': 'Consulted when present',
                'authority_level': 'Low - provides input to CX Champion',
                'prefers': 'Detailed operational demos'
            },

            'recommended_products': [
                {
                    'product': 'QA & Coaching',
                    'zendesk_name': 'Zendesk QA',
                    'url': 'https://www.zendesk.com/service/qa/',
                    'relevance': 'Critical',
                    'why': 'Manual QA sampling misses 95% of interactions and coaching is reactive. When process gaps hide in blind spots, quality suffers and problems escalate.',
                    'addresses_challenge': 'We only QA 5% of tickets - we have no idea what\'s actually happening in most customer interactions'
                },
                {
                    'product': 'Analytics',
                    'zendesk_name': 'Zendesk Explore',
                    'url': 'https://www.zendesk.com/service/analytics/',
                    'relevance': 'Critical',
                    'why': 'Flying blind on agent performance and volume trends means constant firefighting. Real-time dashboards turn reactive ops into proactive optimization.',
                    'addresses_challenge': 'I can\'t tell you why tickets are piling up or which agents need help - we have no real-time visibility'
                },
                {
                    'product': 'Omnichannel Routing',
                    'zendesk_name': 'Zendesk Omnichannel Routing',
                    'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                    'relevance': 'High',
                    'why': 'Manual routing creates uneven workload distribution and long wait times. Intelligent routing optimizes capacity and improves SLA performance.',
                    'addresses_challenge': 'Our forecasting is guesswork - we\'re either overstaffed wasting money or understaffed missing SLAs'
                }
            ]
        },

        'Finance/Procurement Gatekeeper': {
            'job_titles': [
                'CFO',
                'Finance Director',
                'Controller',
                'VP Finance'
            ],
            'reports_to': 'CEO or Board',
            'team_size': 'Finance team (2-10 people)',
            'prevalence': '42% of SMB deals',
            'role_in_deal': 'Budget Approver',

            'goals': [
                'Control costs and maintain budget discipline',
                'Ensure ROI on technology investments',
                'Predictable, manageable cash flow',
                'Avoid surprise costs or overages',
                'Negotiate favorable contract terms'
            ],

            'pain_points': [
                'Support costs growing faster than revenue',
                'Software sprawl - too many subscriptions',
                'Getting nickel-and-dimed with add-on fees',
                'Can\'t justify ROI on existing support tool',
                'Cash flow constraints - can\'t commit to large annual prepays'
            ],

            'challenges_from_gong': [
                'Economic sensitivity - longer approval cycles, more scrutiny',
                'Preference for monthly/quarterly payment terms (cash flow)',
                'ROI justification requirements increasing',
                'Budget frozen or cut',
                'Vendor consolidation pressure'
            ],

            'evaluation_criteria': [
                'Total cost of ownership (license + implementation + training)',
                'Payment terms flexibility (monthly vs. annual)',
                'ROI evidence from similar companies',
                'Contract terms (auto-renewal, cancellation policy)',
                'Price predictability as we scale'
            ],

            'objections': [
                '"Can we really afford this right now?"',
                '"What\'s the payback period?"',
                '"Why is this better than just hiring another agent?"',
                '"Can we do monthly payments instead of annual?"'
            ],

            'key_messages': [
                'Clear ROI: 30% productivity gain = 5-6 month payback',
                'Flexible payment terms available',
                'Predictable per-agent pricing - no surprise fees',
                'Cheaper than hiring: one agent salary = 10+ licenses',
                'Vendor consolidation - replace 3 tools with one'
            ],

            'content_preferences': [
                'ROI calculators',
                'TCO comparisons',
                'Pricing guides',
                'Payment terms options',
                'Reference customers with similar budget profiles'
            ],

            'success_metrics': [
                'Cost per ticket',
                'Support cost as % of revenue',
                'Payback period',
                'Avoided hiring costs',
                'Vendor consolidation savings'
            ],

            'buying_behavior': {
                'decision_speed': 'Gatekeeper (adds 1-2 weeks)',
                'committee_size': 'Solo review or with CEO',
                'authority_level': 'High - can block deals',
                'prefers': 'Financial analysis, minimal sales fluff'
            },

            'recommended_products': [
                {
                    'product': 'Zendesk Suite',
                    'zendesk_name': 'Zendesk Suite',
                    'url': 'https://www.zendesk.com/pricing/support-suite/',
                    'relevance': 'High',
                    'why': 'Managing 5+ separate vendor contracts increases procurement overhead and renewal chaos. Vendor consolidation directly reduces costs and simplifies budgeting.',
                    'addresses_challenge': 'We have too many software subscriptions - I need to consolidate vendors and reduce spend'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'High',
                    'why': 'Support costs growing faster than revenue is unsustainable. With 47% of SMB facing cost pressure, automation offers clear payback: one agent salary funds 10+ licenses.',
                    'addresses_challenge': 'Our support budget is growing faster than revenue - we need ROI or we\'re cutting headcount'
                },
                {
                    'product': 'Analytics',
                    'zendesk_name': 'Zendesk Explore',
                    'url': 'https://www.zendesk.com/service/analytics/',
                    'relevance': 'Medium',
                    'why': 'Without hard metrics, support spend is a black box. Real-time ROI tracking (cost per ticket, deflection rates) justifies budget and identifies waste.',
                    'addresses_challenge': 'I can\'t tell if our support investment is worth it - show me the ROI in dollars'
                }
            ]
        }
    },

    'Commercial': {
        'CX Champion': {
            'job_titles': [
                'VP Customer Service',
                'VP Customer Experience',
                'Director of Customer Support',
                'Head of Global Support',
                'Senior Director CX'
            ],
            'reports_to': 'COO, Chief Customer Officer, or CEO',
            'team_size': '25-100 agents (often multi-region)',
            'prevalence': '92% of Commercial deals',
            'role_in_deal': 'Primary Champion (but needs coalition)',

            'goals': [
                'Scale support operations across regions/brands',
                'Drive 55-60% ticket deflection through self-service + AI',
                'Improve CSAT while reducing cost-per-ticket',
                'Modernize support tech stack (replace legacy tools)',
                'Build self-service culture with customers'
            ],

            'pain_points': [
                'Managing 50-100 agents across multiple teams/shifts',
                'Complex SLA requirements (different per client/tier)',
                'Legacy tools can\'t handle current scale',
                'No unified view across email, chat, phone, social',
                'Executive pressure to reduce costs while improving CX'
            ],

            'challenges_from_gong': [
                'Integration complexity - custom dispatch systems, multi-client data',
                'Self-service culture shift - not just tools, behavioral change',
                'Reporting gaps - need custom dashboards for executives',
                'Process automation needs - not just ticket routing',
                'Skills-based routing for specialized teams',
                'Multi-language support requirements for global teams'
            ],

            'evaluation_criteria': [
                'Enterprise scalability - can this handle 100+ agents and grow to 500?',
                'Advanced automation - intent-based routing, AI-powered triage',
                'Multi-org/multi-brand support',
                'Customization - workflows, fields, automations',
                'Change management support during rollout'
            ],

            'objections': [
                '"We have too many custom requirements"',
                '"Our team is already overwhelmed - can\'t handle a big migration"',
                '"How long will implementation really take?"',
                '"What if our agents hate it?"'
            ],

            'key_messages': [
                'Built for enterprise complexity - multi-org, custom workflows, advanced routing',
                'Change management included - dedicated team to ensure adoption',
                'Phased rollout - start with one team, expand when ready',
                'Agent-loved - 4.6★ rating, faster than legacy tools',
                'Proven at scale - customers with 500+ agents'
            ],

            'content_preferences': [
                'Enterprise customer case studies',
                'Executive briefings with VP-level champions',
                'Analyst reports (Gartner Magic Quadrant)',
                'ROI models for mid-market',
                'Reference calls with similar companies'
            ],

            'success_metrics': [
                'CSAT / NPS',
                'Ticket deflection rate (target: 55-60%)',
                'Cost per ticket',
                'First response time by tier',
                'Agent utilization rate'
            ],

            'buying_behavior': {
                'decision_speed': '75-100 days',
                'committee_size': '6-8 people (CX, IT, Ops, Finance, Procurement, C-Suite)',
                'authority_level': 'Medium - needs buy-in from IT, Finance, Ops',
                'prefers': 'Structured evaluation, proof-of-concept, reference checks'
            },

            'recommended_products': [
                {
                    'product': 'Integrations',
                    'zendesk_name': 'Zendesk Apps & Integrations',
                    'url': 'https://www.zendesk.com/marketplace/',
                    'relevance': 'Critical',
                    'why': 'With 62% of Commercial companies citing integration needs, connecting Salesforce, SAP, and custom systems is make-or-break. Agents lose context switching between 5+ systems.',
                    'addresses_challenge': 'Our agents are toggling between seven different systems to resolve one ticket - we\'re bleeding efficiency'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'Critical',
                    'why': 'Ticket volume is outpacing headcount growth 3:1. With 42% of Commercial facing cost pressure, 40-60% automation rates directly impact the bottom line.',
                    'addresses_challenge': 'We need to cut costs but we\'re drowning in volume - how do we do more with less?'
                },
                {
                    'product': 'Omnichannel Routing',
                    'zendesk_name': 'Zendesk Omnichannel Routing',
                    'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                    'relevance': 'High',
                    'why': 'Multi-tier SLAs (platinum, gold, silver clients) require intelligent routing. Manual assignment misses SLAs and creates uneven workload distribution.',
                    'addresses_challenge': 'We have different SLAs for different customer tiers and can\'t route tickets intelligently - we\'re constantly missing targets'
                },
                {
                    'product': 'Copilot',
                    'zendesk_name': 'Zendesk AI Copilot',
                    'url': 'https://www.zendesk.com/platform/copilot/',
                    'relevance': 'High',
                    'why': 'Cost-per-ticket and CSAT are competing priorities. Copilot delivers both: 25% faster resolution without sacrificing quality or customer satisfaction.',
                    'addresses_challenge': 'We need to reduce handle time but leadership says we can\'t compromise on quality - how do we do both?'
                }
            ]
        },

        'C-Suite Decision Maker': {
            'job_titles': [
                'COO',
                'CEO',
                'Chief Customer Officer',
                'President'
            ],
            'reports_to': 'Board',
            'team_size': 'Entire company (250-1,499 employees)',
            'prevalence': '54% of Commercial deals',
            'role_in_deal': 'Budget Holder (appears late in process)',

            'goals': [
                'Platform consolidation - reduce vendor count',
                'Improve customer retention and LTV',
                'Enable profitable growth',
                'Modernize tech stack to support next 5 years',
                'Data-driven decision making'
            ],

            'pain_points': [
                'Support org using 5-10 different tools (fragmented)',
                'Customer churn tied to poor support experience',
                'Can\'t get clear visibility into support operations',
                'Legacy tools holding back innovation',
                'Board asking tough questions about support ROI'
            ],

            'challenges_from_gong': [
                'Platform vs. point solution debate - prefer vendor consolidation',
                'Strategic investment - need 3-5 year vision',
                'Risk mitigation - big migrations are high stakes',
                'ROI proof for board/investors',
                'Competitive differentiation through CX'
            ],

            'evaluation_criteria': [
                'Strategic platform play - can this replace 3+ tools?',
                'Future-proof - AI roadmap, innovation velocity',
                'Vendor stability and financial health',
                'Implementation risk and timeline',
                'Executive sponsorship and support from vendor'
            ],

            'objections': [
                '"Why not just keep what we have?"',
                '"What\'s the business case for this level of investment?"',
                '"What if this impacts customer experience during transition?"',
                '"Are we backing the right vendor for 5+ years?"'
            ],

            'key_messages': [
                'Platform consolidation - replace 3-5 tools with one',
                'Proven at your scale - 1000+ mid-market customers',
                'AI-first roadmap - built for next 5 years',
                'Risk mitigation - phased rollout, rollback plans',
                'Executive sponsorship - dedicated CSM and EBC support'
            ],

            'content_preferences': [
                'Board-ready business case',
                'Strategic roadmap briefings',
                'Industry analyst validation',
                'Executive roundtables with peers',
                'Financial analyst reports'
            ],

            'success_metrics': [
                'Customer retention rate',
                'Support cost as % of revenue',
                'NPS',
                'Vendor consolidation savings',
                'Time to implement innovation'
            ],

            'buying_behavior': {
                'decision_speed': 'Appears in week 6-8 of deal',
                'committee_size': 'Final approver (reviews deal packaged by team)',
                'authority_level': 'Ultimate - signs off on budget',
                'prefers': 'Concise executive briefing, peer references'
            },

            'recommended_products': [
                {
                    'product': 'Zendesk Suite',
                    'zendesk_name': 'Zendesk Complete Suite',
                    'url': 'https://www.zendesk.com/pricing/support-suite/',
                    'relevance': 'Critical',
                    'why': 'Managing 5+ disconnected tools creates vendor fatigue and renewal chaos. Consolidation reduces costs, simplifies operations, and is a board-level priority.',
                    'addresses_challenge': 'We need to consolidate vendors - managing five different support tools is costing us money and time'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'Critical',
                    'why': 'Churn analysis shows poor support is costing customers. With AI-first strategies on every board agenda, automation directly impacts retention and profitability.',
                    'addresses_challenge': 'Our customer churn is tied to support quality - we need AI to scale without sacrificing experience'
                },
                {
                    'product': 'Analytics',
                    'zendesk_name': 'Zendesk Explore',
                    'url': 'https://www.zendesk.com/service/analytics/',
                    'relevance': 'High',
                    'why': 'Board wants proof support investments are working. Without executive dashboards showing ROI, support is seen as a cost center, not a strategic asset.',
                    'addresses_challenge': 'I can\'t show the board what our support organization is actually delivering - we need real-time metrics'
                }
            ]
        },

        'IT Influencer': {
            'job_titles': [
                'VP IT',
                'Director of IT',
                'Head of Information Security',
                'IT Manager',
                'CISO'
            ],
            'reports_to': 'CTO, COO, or CEO',
            'team_size': '5-25 IT staff',
            'prevalence': '85% of Commercial deals',
            'role_in_deal': 'Co-Champion & Validator (critical path)',

            'goals': [
                'Ensure enterprise-grade security and compliance',
                'Manage integrations and API strategy',
                'Minimize technical debt and shadow IT',
                'Enable IT governance (SSO, user provisioning, audit logs)',
                'Protect customer data and meet regulatory requirements'
            ],

            'pain_points': [
                'Security audits finding vulnerabilities in old tools',
                'Integration sprawl - too many point-to-point connections',
                'Compliance requirements (GDPR, HIPAA, SOC 2, ISO)',
                'Legacy tools without modern APIs',
                'Shadow IT circumventing security policies'
            ],

            'challenges_from_gong': [
                'AI governance scrutiny - how is AI trained? Where is data stored?',
                'Data residency requirements (EU, APAC)',
                'Enterprise integration complexity',
                'Security validation at demo stage (not end of cycle)',
                'Can veto deals if security concerns not addressed'
            ],

            'evaluation_criteria': [
                '**#1 Priority:** Security & compliance (SOC 2 Type 2, ISO 27001, GDPR, HIPAA)',
                'API quality - RESTful, well-documented, versioned',
                'SSO/SAML, SCIM provisioning',
                'Data governance - encryption, residency, retention policies',
                'AI transparency - how models work, what data they use'
            ],

            'objections': [
                '"How do you ensure AI doesn\'t expose sensitive customer data?"',
                '"Can you meet our data residency requirements?"',
                '"What happens if your API changes and breaks our integrations?"',
                '"Do you have SOC 2 Type 2 and penetration test results?"'
            ],

            'key_messages': [
                'Enterprise security built-in - SOC 2 Type 2, ISO 27001, GDPR, HIPAA',
                'AI governance - transparent models, customer data isolation, audit trails',
                'Enterprise APIs - RESTful, 99.9% uptime SLA, versioned',
                'Data residency options - EU, APAC, US regions',
                'Dedicated security documentation for your audit'
            ],

            'content_preferences': [
                'Security whitepapers',
                'Compliance certifications',
                'API documentation and sandbox',
                'Architecture diagrams',
                'Penetration test results (under NDA)'
            ],

            'success_metrics': [
                'Security audit pass rate',
                'Zero data breaches',
                'API uptime and reliability',
                'Integration stability',
                'Compliance certification maintenance'
            ],

            'buying_behavior': {
                'decision_speed': 'Involved at demo stage (week 2-3)',
                'committee_size': 'Works with security team',
                'authority_level': 'High - can veto deals',
                'prefers': 'Technical deep dives, proof-of-concept'
            }
        },

        'Operations Leader': {
            'job_titles': [
                'Director of Service Operations',
                'VP Operations',
                'Workforce Management Manager',
                'Quality Assurance Director',
                'Service Delivery Manager'
            ],
            'reports_to': 'COO or CX Champion',
            'team_size': 'Oversees ops, WFM, QA teams',
            'prevalence': '45% of Commercial deals (EMERGING)',
            'role_in_deal': 'Key Influencer (growing importance)',

            'goals': [
                'Optimize workforce management and capacity planning',
                'Scale QA from <1% to 100% of interactions (AI-powered)',
                'Improve operational efficiency and reduce waste',
                'Real-time visibility into 50-100 agent operations',
                'Data-driven process improvements'
            ],

            'pain_points': [
                'Manual WFM in spreadsheets - can\'t forecast accurately',
                'QA team can only review <1% of interactions manually',
                'No real-time visibility into agent performance',
                'Process bottlenecks not visible until quarterly reviews',
                'Over/understaffing costs millions annually'
            ],

            'challenges_from_gong': [
                'WFM integration requirements - need to connect to existing tools',
                'Quality assurance at scale - AI needed',
                'Real-time operational dashboards',
                'Agent performance analytics and coaching',
                'Multi-team visibility (8+ teams across regions)'
            ],

            'evaluation_criteria': [
                'WFM capabilities or integrations (Verint, Calabrio, NICE)',
                'AI-powered QA to review 100% of interactions',
                'Real-time operational dashboards',
                'Agent performance management tools',
                'Customizable reporting for different stakeholders'
            ],

            'objections': [
                '"Will this integrate with our WFM platform?"',
                '"Can your AI QA handle our complex quality rubrics?"',
                '"Is reporting flexible enough for our needs?"',
                '"What if agents game the new metrics?"'
            ],

            'key_messages': [
                'AI-powered QA - review 100% of interactions, not just 1%',
                'WFM integrations - Verint, Calabrio, NICE, custom APIs',
                'Real-time ops center - visibility into all teams',
                'Agent coaching tools - turn QA insights into performance gains',
                'Proven ROI - 15-20% efficiency gains from better WFM'
            ],

            'content_preferences': [
                'WFM integration guides',
                'QA automation case studies',
                'Operational efficiency benchmarks',
                'Workforce optimization ROI models'
            ],

            'success_metrics': [
                'Schedule adherence %',
                'Occupancy rate',
                'QA score trends',
                'Cost per interaction',
                'Agent attrition rate'
            ],

            'buying_behavior': {
                'decision_speed': 'Influential throughout process',
                'committee_size': 'Works closely with CX Champion',
                'authority_level': 'Medium-High - can influence decision',
                'prefers': 'Operational deep dives, metrics-focused demos'
            }
        },

        'Finance/Procurement Gatekeeper': {
            'job_titles': [
                'CFO',
                'VP Finance',
                'Procurement Director',
                'Vendor Management',
                'Director of Procurement'
            ],
            'reports_to': 'CEO or Board',
            'team_size': 'Finance/procurement team',
            'prevalence': '58% of Commercial deals',
            'role_in_deal': 'Gatekeeper (appears at demo stage, not just contracting)',

            'goals': [
                'Negotiate favorable contract terms',
                'Ensure compliance with procurement policies',
                'Vendor risk management and due diligence',
                'Budget optimization and cost control',
                'Vendor consolidation to reduce complexity'
            ],

            'pain_points': [
                'Software sprawl - managing 100+ vendor relationships',
                'Shadow IT spending not going through procurement',
                'Unfavorable contract terms inherited from previous deals',
                'Vendor financial instability risks',
                'Lack of visibility into true total cost'
            ],

            'challenges_from_gong': [
                'Procurement appearing 40% earlier - at demo stage, not just negotiation',
                'Formal RFP/RFI processes - need structured responses',
                'Vendor risk assessment requirements',
                '3+ vendor comparison mandates',
                'More scrutiny on contract terms and pricing'
            ],

            'evaluation_criteria': [
                'Total cost of ownership (licensing, implementation, training, support)',
                'Contract terms (auto-renewal, cancellation, SLAs, penalties)',
                'Vendor financial stability (Dun & Bradstreet, funding)',
                'Pricing scalability (what happens at 2x, 3x growth?)',
                'Reference checks from procurement peers'
            ],

            'objections': [
                '"Your pricing doesn\'t fit our budget model"',
                '"We need more favorable contract terms"',
                '"How do we know you\'ll be around in 5 years?"',
                '"Why are you more expensive than [Competitor]?"'
            ],

            'key_messages': [
                'Transparent pricing - no hidden fees, predictable scaling',
                'Flexible contract terms available for enterprises',
                'Financially stable - [funding status, customer count]',
                'TCO advantage - replace 3 tools, reduce implementation costs',
                'Procurement-ready - RFP templates, vendor risk docs, references'
            ],

            'content_preferences': [
                'RFP response templates',
                'Vendor risk assessment questionnaires',
                'Financial statements and stability proof',
                'Pricing comparison matrices',
                'Procurement peer references'
            ],

            'success_metrics': [
                'Cost savings vs. budget',
                'Contract compliance',
                'Vendor consolidation progress',
                'Risk mitigation',
                'Favorable payment terms achieved'
            ],

            'buying_behavior': {
                'decision_speed': 'Gatekeeper (adds 2-4 weeks)',
                'committee_size': 'Works with legal and finance',
                'authority_level': 'High - can block deals',
                'prefers': 'Formal RFP process, detailed financial analysis'
            }
        }
    },

    'Digital': {
        'Founder/Owner': {
            'job_titles': [
                'Founder',
                'CEO',
                'Owner',
                'Managing Director'
            ],
            'reports_to': 'Self',
            'team_size': '1-10 employees total',
            'prevalence': '88% of Digital deals',
            'role_in_deal': 'Sole Decision Maker',

            'goals': [
                'Get support tools running quickly with zero IT help',
                'Keep costs low - every dollar counts',
                'Deliver professional customer service despite small team',
                'Scale support as business grows without hiring',
                'Automate everything possible'
            ],

            'pain_points': [
                'Wearing too many hats - no time to learn complex tools',
                'Budget constraints - need maximum value at minimum cost',
                'No dedicated support staff - everyone does support',
                'Email overload - customers expect faster response',
                'Can\'t afford enterprise tools but need professional features'
            ],

            'challenges_from_gong': [
                'Price sensitivity - need startup/small business pricing',
                'Self-service implementation required - no IT department',
                'Evaluating against Zoho Desk, HubSpot Service Hub, Freshdesk',
                'Integration needs: Moodle (education), Respond.io (messaging), basic CRMs',
                'Common verticals: tutoring services, education portals, healthcare services',
                'Mobile-first needs - managing support on the go',
                'Need immediate value - can\'t wait months for ROI'
            ],

            'evaluation_criteria': [
                'Price (must be under $50-100/month)',
                'Setup time (must be live in hours, not weeks)',
                'Mobile app quality',
                'No learning curve - intuitive like consumer apps',
                'Free trial to test before buying'
            ],

            'objections': [
                '"This is too expensive for our size"',
                '"I\'m already using Zoho Desk - why switch?"',
                '"Looks complicated - don\'t have time to learn"',
                '"Do I really need this or can I just use email?"',
                '"What if my business doesn\'t grow as expected?"',
                '"Will this integrate with my student portal/LMS?"'
            ],

            'key_messages': [
                'Special pricing for startups - as low as $19/month',
                'Setup in 15 minutes - no technical skills required',
                'Mobile app lets you support customers anywhere',
                'Start free, pay as you grow',
                'Thousands of solo founders trust us'
            ],

            'content_preferences': [
                'Short video tutorials (2-3 minutes)',
                'Quick start guides',
                'Founder testimonials from similar businesses',
                'Pricing calculator',
                '14-day free trial'
            ],

            'success_metrics': [
                'Time saved per day',
                'Customer response time',
                'Cost per month',
                'Customer satisfaction',
                'Tool adoption by team'
            ],

            'buying_behavior': {
                'decision_speed': '7-14 days',
                'committee_size': '1 person (solo decision)',
                'authority_level': 'Complete - no approvals needed',
                'prefers': 'Self-service trial, no sales calls, transparent pricing'
            },

            'recommended_products': [
                {
                    'product': 'Messaging',
                    'zendesk_name': 'Zendesk Messaging',
                    'url': 'https://www.zendesk.com/service/messaging/',
                    'relevance': 'Critical',
                    'why': 'Customers expect instant responses on WhatsApp and social. With 45% of Digital companies prioritizing messaging, it\'s where customers are and you need to be there.',
                    'addresses_challenge': 'My customers want to message me on WhatsApp and Instagram, not email - I\'m missing inquiries'
                },
                {
                    'product': 'Integrations',
                    'zendesk_name': 'Zendesk Apps & Integrations',
                    'url': 'https://www.zendesk.com/marketplace/',
                    'relevance': 'Critical',
                    'why': 'With 48% of Digital companies citing integration needs, connecting Moodle, Respond.io, and basic CRMs is critical. No IT team means pre-built connectors are essential.',
                    'addresses_challenge': 'I need to connect to my tools but I don\'t have an IT person - it needs to just work'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'High',
                    'why': 'With 44% of Digital facing cost pressure, hiring isn\'t an option. AI lets you scale support without payroll increases - answering 24/7 for less than a part-timer.',
                    'addresses_challenge': 'I can\'t afford to hire someone but customers need answers at midnight - what do I do?'
                },
                {
                    'product': 'Knowledge Base',
                    'zendesk_name': 'Zendesk Help Center',
                    'url': 'https://www.zendesk.com/service/help-center/',
                    'relevance': 'High',
                    'why': 'When you\'re answering the same questions 20 times a day, you\'re losing time on growth activities. Self-service frees you from repetitive work.',
                    'addresses_challenge': 'I keep answering "how do I reset my password" all day - customers should be able to figure this out themselves'
                }
            ]
        },

        'Customer Service Generalist': {
            'job_titles': [
                'Customer Success Manager',
                'Office Manager',
                'Operations Coordinator',
                'Customer Service Rep'
            ],
            'reports_to': 'Founder/Owner',
            'team_size': 'Handles support solo or with 1-2 others',
            'prevalence': '45% of Digital deals',
            'role_in_deal': 'User/Influencer (recommends to founder)',

            'goals': [
                'Respond to customers quickly across email, chat, social',
                'Keep founder happy by handling support independently',
                'Track customer issues and spot patterns',
                'Look professional despite being a small team',
                'Reduce repetitive questions with self-service'
            ],

            'pain_points': [
                'Juggling multiple communication channels',
                'No system - using personal email and spreadsheets',
                'Can\'t find previous conversations with customers',
                'No visibility into response times or customer satisfaction',
                'Spending too much time on the same questions'
            ],

            'challenges_from_gong': [
                'Need omnichannel - customers reach out everywhere',
                'Knowledge base gaps - no organized help content',
                'No collaboration tools when teammates help',
                'Manual work - copying/pasting same answers',
                'No reporting for the founder'
            ],

            'evaluation_criteria': [
                'Easy to use daily - not intimidating',
                'Handles email, chat, and social in one place',
                'Can create simple help articles',
                'Affordable on tight budget',
                'Quick to learn - ideally no training needed'
            ],

            'objections': [
                '"Will the founder approve the cost?"',
                '"Looks too complicated for our small team"',
                '"We already use email, why change?"',
                '"What if I can\'t figure it out?"'
            ],

            'key_messages': [
                'All customer conversations in one inbox',
                'Built for small teams - dead simple to use',
                'Free help center builder included',
                'Get started in minutes, not hours',
                'Live chat support to help you succeed'
            ],

            'content_preferences': [
                'Video walkthroughs',
                'Getting started checklist',
                'Templates for common responses',
                'Small business case studies',
                'Live onboarding help'
            ],

            'success_metrics': [
                'Response time',
                'Number of conversations handled',
                'Customer satisfaction ratings',
                'Time saved with canned responses',
                'Help center article views'
            ],

            'buying_behavior': {
                'decision_speed': 'Recommends to founder (adds 1-2 weeks)',
                'committee_size': 'Needs founder approval',
                'authority_level': 'Low - influencer only',
                'prefers': 'Trial before pitching to founder'
            },

            'recommended_products': [
                {
                    'product': 'Messaging',
                    'zendesk_name': 'Zendesk Messaging',
                    'url': 'https://www.zendesk.com/service/messaging/',
                    'relevance': 'Critical',
                    'why': 'Switching between 4+ apps to check messages is exhausting and you miss things. One inbox means nothing falls through the cracks.',
                    'addresses_challenge': 'I\'m constantly switching between email, WhatsApp, Facebook - I can\'t keep up with all these tabs'
                },
                {
                    'product': 'Knowledge Base',
                    'zendesk_name': 'Zendesk Help Center',
                    'url': 'https://www.zendesk.com/service/help-center/',
                    'relevance': 'Critical',
                    'why': 'Answering the same questions 15 times a day steals time from important work. When customers can self-serve, you can focus on what matters.',
                    'addresses_challenge': 'I\'m typing the same answers over and over - there has to be a better way'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'High',
                    'why': 'Copy-pasting canned responses isn\'t sustainable. Automation handles the repetitive stuff so you can spend time on customers who actually need help.',
                    'addresses_challenge': 'I\'m just copy-pasting the same answers all day - it feels like robot work'
                },
                {
                    'product': 'Copilot',
                    'zendesk_name': 'Zendesk AI Copilot',
                    'url': 'https://www.zendesk.com/platform/copilot/',
                    'relevance': 'Medium',
                    'why': 'When you\'re the only support person, you don\'t have anyone to ask for help. Copilot is like having an experienced teammate suggesting answers.',
                    'addresses_challenge': 'I\'m not sure how to answer some of these questions and there\'s no one to ask for help'
                }
            ]
        }
    },

    'Enterprise': {
        'CX Executive': {
            'job_titles': [
                'SVP Customer Experience',
                'Chief Customer Officer',
                'VP Global Customer Support',
                'Head of Customer Success & Support'
            ],
            'reports_to': 'CEO or President',
            'team_size': '100-500+ agents across multiple regions',
            'prevalence': '95% of Enterprise deals',
            'role_in_deal': 'Executive Sponsor & Final Approver',

            'goals': [
                'Transform customer experience into competitive advantage',
                'Reduce cost-to-serve while improving NPS by 15+ points',
                'Consolidate fragmented CX tech stack (8-15 tools)',
                'Enable global support across 20+ languages',
                'Prove ROI to board with data-driven CX metrics'
            ],

            'pain_points': [
                'Legacy tools can\'t scale - platform limitations at 500+ agents',
                'CX data siloed across systems - no unified customer view',
                'Board pressure for efficiency - "do more with less"',
                'Change fatigue - teams burned out from failed transformations',
                'Competitive threat - competitors have better digital CX'
            ],

            'challenges_from_gong': [
                'Multi-year digital transformation roadmaps',
                'Contract renewals - optimizing costs while improving CX',
                'Global rollout complexity - 5+ regions, compliance requirements',
                'Government/public sector requirements - accessibility, transparency',
                'BPO/outsourcing support operations - quotation management, travel',
                'Change management at scale - 100s of agents to train',
                'Integration with enterprise systems (SAP, Oracle, ServiceNow, X plan)',
                'Executive buy-in for $500K-$2M+ investment'
            ],

            'evaluation_criteria': [
                'Enterprise scalability - proven at 1000+ agent deployments',
                'Strategic partnership - not just a vendor',
                'Global support - 24/7 enterprise SLAs, multi-language',
                'Gartner/Forrester positioning - top quadrant placement',
                'Change management & consulting services included'
            ],

            'objections': [
                '"We\'ve already invested millions in our current platform"',
                '"Our contract is up for renewal - need to cut costs, not increase them"',
                '"Too risky to migrate 500+ agents"',
                '"Government procurement requirements make this a 9-12 month process"',
                '"Our business is too complex for out-of-box solutions"',
                '"How long will implementation really take?"'
            ],

            'key_messages': [
                'Gartner Leader - proven at Fortune 500 scale',
                'Migration de-risked - dedicated team, proven methodology',
                '18-24 month ROI with 25-30% efficiency gains',
                'White-glove change management included',
                'Reference customers: [major enterprise names]'
            ],

            'content_preferences': [
                'Executive briefings with CCOs from similar companies',
                'Analyst reports (Gartner, Forrester, Constellation)',
                'Total Economic Impact study',
                'Multi-year transformation roadmap',
                'Board-ready business case'
            ],

            'success_metrics': [
                'NPS improvement',
                'Cost-to-serve reduction',
                'Agent productivity (cases per agent)',
                'Platform consolidation (tools eliminated)',
                'Customer lifetime value impact'
            ],

            'buying_behavior': {
                'decision_speed': '6-12 months',
                'committee_size': '10-15 people (CX, IT, Finance, Procurement, Legal, Security, Operations)',
                'authority_level': 'Executive Sponsor - drives but needs coalition',
                'prefers': 'Structured RFP, POC with 50+ agents, multi-phase rollout'
            },

            'recommended_products': [
                {
                    'product': 'Integrations',
                    'zendesk_name': 'Zendesk Enterprise Integration Platform',
                    'url': 'https://www.zendesk.com/marketplace/',
                    'relevance': 'Critical',
                    'why': 'Global transformation depends on connecting SAP, ServiceNow, and regional systems across 5+ countries. With 40% of Enterprise citing integration complexity, this is the foundation.',
                    'addresses_challenge': 'We have SAP in EMEA, Oracle in APAC, and ServiceNow in the US - we can\'t operate in silos anymore'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'Critical',
                    'why': 'Board wants proof that CX investments deliver ROI. With 38% of Enterprise facing cost pressure, automation at Fortune 500 scale (100K+ daily conversations) is table stakes.',
                    'addresses_challenge': 'The board wants to know why we need 500 agents - prove we can reduce cost-to-serve without hurting NPS'
                },
                {
                    'product': 'Contact Center',
                    'zendesk_name': 'Zendesk Contact Center',
                    'url': 'https://www.zendesk.com/service/contact-center/',
                    'relevance': 'High',
                    'why': 'Supporting 20+ languages across 8 time zones requires enterprise-grade infrastructure. 99.99% uptime isn\'t optional when downtime costs millions.',
                    'addresses_challenge': 'We need to support customers in 20 languages across every time zone - our current tools can\'t scale globally'
                },
                {
                    'product': 'Analytics',
                    'zendesk_name': 'Zendesk Explore',
                    'url': 'https://www.zendesk.com/service/analytics/',
                    'relevance': 'High',
                    'why': 'Quarterly board meetings demand hard numbers on CX ROI. Without unified analytics across regions and brands, you\'re presenting gut feelings, not data.',
                    'addresses_challenge': 'The board keeps asking what our CX investment is delivering - I need data that shows impact on revenue and retention'
                }
            ]
        },

        'Enterprise IT Architect': {
            'job_titles': [
                'Enterprise Architect',
                'VP Technology',
                'Chief Information Officer',
                'Director Enterprise Applications'
            ],
            'reports_to': 'CIO or CTO',
            'team_size': 'IT department of 50-200+',
            'prevalence': '85% of Enterprise deals',
            'role_in_deal': 'Technical Approver & Gatekeeper',

            'goals': [
                'Ensure enterprise architecture alignment and standards',
                'Reduce technical debt and platform sprawl',
                'Maintain security, compliance, and governance',
                'Enable scalability and business continuity',
                'Minimize IT operational burden'
            ],

            'pain_points': [
                'Shadow IT - departments buying SaaS without IT approval',
                'Integration complexity - 200+ enterprise systems',
                'Security and compliance risks at scale',
                'Aging legacy systems that need replacement',
                'Limited IT resources for custom development'
            ],

            'challenges_from_gong': [
                'Enterprise integration requirements - SSO, SCIM, APIs, webhooks',
                'Security and compliance - SOC 2, ISO, HIPAA, GDPR, FedRAMP',
                'Disaster recovery and business continuity planning',
                'Data residency and sovereignty requirements',
                'Professional services for custom integrations'
            ],

            'evaluation_criteria': [
                'Enterprise security certifications (SOC 2 Type 2, ISO 27001, FedRAMP)',
                'Integration architecture - REST APIs, webhooks, SCIM, enterprise SSO',
                'Scalability and performance - SLAs for 99.99% uptime',
                'Data governance - encryption, residency, retention',
                'Professional services team for complex implementations'
            ],

            'objections': [
                '"Does this meet our enterprise security standards?"',
                '"How will this integrate with our SAP/Oracle/ServiceNow/X plan environment?"',
                '"What\'s the total cost of implementation and maintenance?"',
                '"Can you handle our government data residency and compliance requirements?"',
                '"Do you have pre-built integrations for financial services BPO workflows?"'
            ],

            'key_messages': [
                'Enterprise-grade security - SOC 2 Type 2, ISO 27001, FedRAMP authorized',
                'Pre-built enterprise integrations - SAP, Oracle, ServiceNow',
                '99.99% uptime SLA with enterprise support',
                'Global data residency options (US, EU, APAC)',
                'Dedicated solutions architect for implementation'
            ],

            'content_preferences': [
                'Enterprise architecture diagrams',
                'Security and compliance documentation',
                'API and integration documentation',
                'Technical deep-dive sessions',
                'Reference architectures from similar enterprises'
            ],

            'success_metrics': [
                'System uptime and performance',
                'Security audit pass rate',
                'Integration stability',
                'IT ticket reduction',
                'Platform consolidation achieved'
            ],

            'buying_behavior': {
                'decision_speed': '2-4 months technical evaluation',
                'committee_size': 'IT architecture board (5-8 people)',
                'authority_level': 'Can block - must approve architecture',
                'prefers': 'Technical POC, architecture review, security assessment'
            },

            'recommended_products': [
                {
                    'product': 'Enterprise Security',
                    'zendesk_name': 'Zendesk Enterprise Security & Compliance',
                    'url': 'https://www.zendesk.com/product/security/',
                    'relevance': 'Critical',
                    'why': 'Failed audits block enterprise deals and expose regulatory risk. With GDPR, HIPAA, and FedRAMP requirements, compliance isn\'t optional—it\'s the price of entry.',
                    'addresses_challenge': 'Our compliance team won\'t approve any tool that isn\'t SOC 2 and ISO certified with regional data residency'
                },
                {
                    'product': 'Enterprise APIs',
                    'zendesk_name': 'Zendesk Enterprise APIs',
                    'url': 'https://developer.zendesk.com/api-reference/',
                    'relevance': 'Critical',
                    'why': 'Enterprise architecture depends on connecting SAP, Oracle, and ServiceNow. With 40% of Enterprise citing integration needs, robust APIs and pre-built connectors are non-negotiable.',
                    'addresses_challenge': 'We need to integrate with systems that don\'t have out-of-box connectors - show me your API documentation'
                },
                {
                    'product': 'Professional Services',
                    'zendesk_name': 'Zendesk Professional Services',
                    'url': 'https://www.zendesk.com/services/',
                    'relevance': 'High',
                    'why': 'Global rollouts spanning 12-18 months can\'t rely on self-service. Dedicated solutions architects prevent costly mistakes and accelerate time-to-value.',
                    'addresses_challenge': 'We tried to do our last implementation ourselves and it took two years - we need experts this time'
                }
            ]
        },

        'Global Operations Leader': {
            'job_titles': [
                'VP Global Operations',
                'SVP Service Delivery',
                'Head of Workforce Management',
                'Director Global Support Operations'
            ],
            'reports_to': 'CX Executive or COO',
            'team_size': 'Oversees 100-500+ agents globally',
            'prevalence': '72% of Enterprise deals',
            'role_in_deal': 'Key Influencer - operational approval needed',

            'goals': [
                'Optimize global workforce across time zones and regions',
                'Drive operational excellence - 95%+ SLA compliance',
                'Reduce operational costs by 20-30%',
                'Scale operations without proportional headcount growth',
                'Standardize processes across regions'
            ],

            'pain_points': [
                'Workforce management complexity - scheduling 100s across time zones',
                'Process inconsistency across regions',
                'Quality assurance at scale - can\'t review enough interactions',
                'Reporting complexity - different systems per region',
                'Cost pressure - prove efficiency gains'
            ],

            'challenges_from_gong': [
                'Advanced workforce management - AI forecasting, skills-based routing',
                'Quality management at scale - automated QA, coaching workflows',
                'Global process standardization across regions',
                'Real-time operational visibility and alerting',
                'Prove ROI - efficiency metrics, cost-per-ticket reduction'
            ],

            'evaluation_criteria': [
                'Workforce management capabilities or integrations',
                'Quality assurance and coaching tools at scale',
                'Global reporting and real-time dashboards',
                'Automation capabilities - routing, triage, responses',
                'Proven ROI from similar-sized deployments'
            ],

            'objections': [
                '"Our operations are too complex for standard solutions"',
                '"Will this work across our 12 global sites?"',
                '"How long until we see efficiency gains?"',
                '"What if it disrupts current operations?"'
            ],

            'key_messages': [
                'Enterprise WFM integration - Nice, Verint, Calabrio',
                'AI-powered quality management - review 100% of interactions',
                'Global deployment proven - 20+ languages, all time zones',
                '25-30% efficiency gains within 12 months',
                'Phased rollout to minimize disruption'
            ],

            'content_preferences': [
                'Operational metrics case studies',
                'WFM integration documentation',
                'Global deployment playbooks',
                'ROI calculator for enterprise scale',
                'Ops leader peer references'
            ],

            'success_metrics': [
                'SLA compliance rate',
                'Cost per interaction',
                'Agent utilization rate',
                'Quality assurance scores',
                'Workforce efficiency gains'
            ],

            'buying_behavior': {
                'decision_speed': '3-6 months evaluation',
                'committee_size': 'Works with CX Executive and regional leaders',
                'authority_level': 'High influence - operational approval critical',
                'prefers': 'Operational deep dives, metrics analysis, phased POC'
            },

            'recommended_products': [
                {
                    'product': 'Contact Center',
                    'zendesk_name': 'Zendesk Contact Center',
                    'url': 'https://www.zendesk.com/service/contact-center/',
                    'relevance': 'Critical',
                    'why': 'Scheduling 500 agents across 8 time zones without WFM integration is chaos. With 21% of Enterprise prioritizing contact center, enterprise-grade infrastructure is essential.',
                    'addresses_challenge': 'We\'re managing global shifts in spreadsheets - we need WFM that integrates with Nice and handles 20 languages'
                },
                {
                    'product': 'Omnichannel Routing',
                    'zendesk_name': 'Zendesk Omnichannel Routing',
                    'url': 'https://www.zendesk.com/service/omnichannel-routing/',
                    'relevance': 'Critical',
                    'why': 'Missing 95% SLA targets damages client relationships and costs penalties. Intelligent routing with capacity management is the only way to maintain enterprise-level performance.',
                    'addresses_challenge': 'We\'re missing SLAs because tickets sit in queues while agents are idle in other queues - routing is broken'
                },
                {
                    'product': 'QA & Analytics',
                    'zendesk_name': 'Zendesk QA & Explore',
                    'url': 'https://www.zendesk.com/service/qa/',
                    'relevance': 'High',
                    'why': 'Manual QA sampling catches less than 1% of problems. When process gaps hide across 8 sites and 20 languages, AI-powered 100% review is the only way to identify issues.',
                    'addresses_challenge': 'Our QA team can only review 1% of calls - we have no idea what quality looks like in Manila or Warsaw'
                },
                {
                    'product': 'AI Agents',
                    'zendesk_name': 'Zendesk AI Agents',
                    'url': 'https://www.zendesk.com/platform/ai-agents/',
                    'relevance': 'High',
                    'why': 'Leadership wants to reduce cost-per-ticket by 30% without hurting CSAT. Automation at scale is the only path to that math.',
                    'addresses_challenge': 'Finance wants us to cut cost-per-ticket by 30% but we can\'t reduce quality - how do we do both?'
                }
            ]
        }
    }
}

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
