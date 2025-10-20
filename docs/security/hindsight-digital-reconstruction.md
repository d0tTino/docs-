---
title: "Hindsight is 20/20: Why Digital Reconstruction Succeeds Where Predictive Surveillance Fails"
tags: [security, research]
project: docs-hub
updated: 2025-10-20
---
--8<-- "_snippets/disclaimer.md"

[[toc]]

# Hindsight is 20/20: Why Digital Reconstruction Succeeds Where Predictive Surveillance Fails

## Executive Summary: Why Hindsight Beats Prediction in a Digital Age
United States security and law enforcement institutions face a defining paradox of the digital age: they demonstrate remarkable proficiency in using vast troves of online and electronic data to reconstruct the planning and execution of violent attacks after they occur, yet they consistently fail to prevent these same incidents through proactive, large-scale monitoring. Post-incident investigations rapidly assemble digital mosaics from social media, communications, and location data to build compelling narratives for prosecution and intelligence analysis. In contrast, pre-incident prevention efforts, often framed as a search for "needles in a haystack," have yielded little success despite massive technological investment, raising profound questions about the efficacy and legitimacy of dragnet surveillance.

This report argues that this asymmetry is not a paradox to be solved but an inevitable outcome of four intersecting and mutually reinforcing constraints that fundamentally separate the tasks of reconstruction and prediction. The perceived failure of predictive systems is not a temporary technological shortcoming but a structural reality rooted in mathematics, law, human behavior, and operational design.

First, the enterprise of prediction is constrained by mathematical reality. Targeted violence is an exceptionally rare event, with a base rate on the order of one incident per million person-years. As dictated by Bayesian probability, any system designed to detect such a rare event—regardless of its technical sophistication or the power of its algorithms—will inevitably produce a crippling number of false positives for every true threat it identifies. Even a hypothetical system with 99% sensitivity and 99.9% specificity would generate over a thousand false alarms for every valid alert, creating an operationally impossible triage burden. This "base-rate problem" is not a flaw in the technology but a fundamental mathematical limit on its utility.

Second, the legal framework of the United States is designed to facilitate focused investigation while strictly limiting speculative monitoring. The Fourth Amendment, as affirmed by the Supreme Court in Carpenter v. United States, erects a high wall—the warrant requirement based on probable cause—around sensitive digital data like long-term location history. This standard is readily met after an attack, when investigators have a specific crime and specific suspects. It is, by design, nearly impossible to meet before an attack, when there is only generalized suspicion. Statutory authorities like Section 702 of the Foreign Intelligence Surveillance Act (FISA) and policy frameworks governing the purchase of commercially available information (CAI) create narrow, complex, and contested pathways for proactive collection, but they do not erase this fundamental constitutional asymmetry. The law is structured to enable reconstruction and impede prediction.

Third, the sociotechnical reality of how threats surface contradicts the logic of dragnet surveillance. Empirical analysis of both averted and completed attacks by the U.S. Secret Service's National Threat Assessment Center (NTAC) and the FBI reveals that actionable intelligence for prevention overwhelmingly originates from human reporting, not automated systems. Most individuals who plan violence exhibit observable concerning behaviors and "leak" their intent to others in their social network—peers, family, classmates, or colleagues. The critical failure point in completed attacks is not a failure to detect a hidden signal, but a failure of bystanders to report an observable one. The prevention challenge is therefore not primarily a technical problem of data collection, but a social problem of encouraging and facilitating human reporting.

Fourth, the operational pipeline for violence prevention is fundamentally incompatible with the output of a dragnet system. The established best practice for prevention is Behavioral Threat Assessment and Management (BTAM), a qualitative, context-rich, and low-volume process conducted by multidisciplinary teams. BTAM is designed to carefully assess a small number of human-vetted referrals. A dragnet surveillance system, by contrast, produces a high-volume, context-poor stream of quantitative alerts. Attempting to feed the output of the latter into the former would create an "impedance mismatch," overwhelming the BTAM system with false positives and rendering it incapable of performing its core function of deep, contextual assessment.

In conclusion, the disparity between post-incident reconstruction and pre-incident prevention is the logical result of a system governed by these four constraints. Reconstruction is a legally sanctioned, mathematically simple, focused search for specific evidence of a known event. Prediction is a legally constrained, mathematically intractable, unfocused search for a rare signal in a sea of noise, a signal that is most often revealed to people, not machines. Effective public policy for preventing targeted violence must therefore pivot away from the alluring but illusory promise of technological omniscience. Instead, it must focus on strengthening the human-centric ecosystem of prevention: educating communities to recognize and report warning signs, empowering multidisciplinary threat assessment teams with the resources to intervene effectively, and employing rights-compatible legal tools that are targeted, specific, and initiated only on the basis of individualized concern.

## Section 1: The Tyranny of the Base Rate — Mathematical Barriers to Prediction
The ambition to prevent targeted violence through the automated monitoring of online data rests on the assumption that with sufficient data and sophisticated algorithms, we can reliably identify individuals on a pathway to violence. This assumption, however, collides with a fundamental and unforgiving mathematical principle: the base-rate problem. For any rare event, the probability that a positive signal from a detection system is a true positive—its positive predictive value (PPV)—is often vanishingly small, even if the system itself is highly accurate. This section explains this principle, models its stark consequences for violence prediction, and quantifies the unmanageable operational burden it creates.

### 1.1 Explainer: The Base-Rate Problem in Violence Prediction
To understand the challenge of predicting targeted violence, it is useful to consider an analogy from medical diagnostics. Imagine a rare disease that affects 1 in 100,000 people (a base rate of 0.001%). A new screening test is developed that is remarkably accurate: it correctly identifies 99% of people who have the disease (99% sensitivity) and correctly identifies 99.9% of people who do not have the disease (99.9% specificity). If a person tests positive, what is the probability they actually have the disease?

Intuition suggests the probability is high, given the test's accuracy. The mathematics of Bayesian inference, however, reveals a different reality. In a population of 10 million people:

- **True positives:** 100 people have the disease. The test correctly identifies 99 of them (100 × 0.99).
- **False positives:** 9,999,900 people do not have the disease. The test incorrectly identifies 0.1% of them as positive, resulting in approximately 10,000 false alarms (9,999,900 × 0.001).

Therefore, for every 10,099 positive tests (99 true positives + 10,000 false positives), only 99 are correct. The positive predictive value (PPV)—the probability that a positive result is a true positive—is just 99 ÷ 10,099, or about 0.98%. Despite the test's high accuracy, over 99% of positive alerts are wrong.

This same logic governs the prediction of targeted violence. Targeted violence is a statistically rare event. While precise figures are difficult to obtain, plausible estimates place the annual base rate for an individual planning or committing such an act in the range of 1 in 100,000 (10^-5) to 1 in 10,000,000 (10^-7) per person-year. Any system, human or machine, that attempts to predict this outcome from general population data will be subject to the same mathematical constraints as the medical test. The PPV, which represents the probability that a person flagged by a surveillance system is a genuine threat, is the most critical metric for operational utility. A low PPV means that investigators will be forced to spend the vast majority of their time and resources investigating false leads.

### 1.2 Modeling PPV and Investigator Workload
To quantify this challenge, we can model the PPV of a hypothetical violence prediction system using the standard Bayesian formula:

\[
\text{PPV} = \frac{\text{Sensitivity} \times \text{Base Rate}}{\text{Sensitivity} \times \text{Base Rate} + (1 - \text{Specificity}) \times (1 - \text{Base Rate})}
\]

The following analysis models the PPV and resulting investigator workload across a range of plausible parameters, consistent with guidance from the National Academies on evaluating predictive systems. We assume a surveillance system monitoring a population of 100 million U.S. adults.

**Scenario analysis assumptions:**

- **Base rates:** 10^-5 (1,000 true positives/year), 10^-6 (100 true positives/year), and 10^-7 (10 true positives/year).
- **Sensitivity (true positive rate):** 70% to 99%.
- **Specificity (true negative rate):** 95% to 99.9%.

The results, visualized in the plots described in Appendix B, are stark. PPV is overwhelmingly driven by the base rate and specificity. Even with a sensitivity of 90% and an exceptionally high specificity of 99.9%, the PPV remains below 1% for a base rate of 10^-5 and collapses to less than 0.1% for a base rate of 10^-6.

This low PPV translates directly into an unsustainable investigative workload, as shown in Table 1.1. The table calculates the number of false positive alerts an agency would need to triage for every true positive it correctly identifies, assuming 90% sensitivity.

**Table 1.1: Investigator Workload (False Positives per True Positive) at 90% Sensitivity**

| Specificity | Base Rate 10^-5 | Base Rate 10^-6 | Base Rate 10^-7 |
|-------------|-----------------|-----------------|-----------------|
| 95.0%       | 5,556           | 55,556          | 555,556         |
| 99.0%       | 1,111           | 11,111          | 111,111         |
| 99.5%       | 556             | 5,556           | 55,556          |
| 99.9%       | 111             | 1,111           | 11,111          |

Even under the most optimistic scenario—a system with 99.9% specificity screening for an event with a base rate of 10^-5—investigators would need to clear 111 false alarms to find a single true threat. For a more realistic base rate of 10^-6 (100 attacks per year in a population of 100 million), that number explodes to over 1,100 false leads per true positive. In this scenario, the system would generate approximately 90 true positive alerts and 100,000 false positive alerts annually. The resources required to meaningfully investigate 100,000 potential threats per year are beyond the capacity of any law enforcement or intelligence agency.

### 1.3 Distinguishing the "Problem" from the "Fallacy"
It is crucial to distinguish the mathematical "base-rate problem" from the cognitive "base rate fallacy." The fallacy is a well-documented human bias where individuals tend to underweight statistical base rates and overweight salient, case-specific information. The problem, however, is an objective, mathematical property of the prediction task itself when the outcome is rare.

A common myth in policy circles is that advances in artificial intelligence and machine learning can "solve" the prediction problem. This is a fundamental misunderstanding. While AI may process data at a scale and speed humans cannot, and may even be designed to avoid the cognitive "fallacy," it cannot defy the mathematical "problem." The formulas for PPV are universal. The policy debate must therefore shift its focus away from the myth of a perfectible predictive algorithm and toward the fact of its mathematical limitations in this domain.

Furthermore, dragnet monitoring systems are inherently deprived of the most predictive data points. Decades of violence risk assessment research have consistently shown that static, historical factors—especially a prior history of violence—are the most powerful predictors of future violence. A dragnet system, by definition, monitors a general population for whom such documented risk factors are absent. It is forced to rely on much weaker, dynamic, and often ambiguous signals, such as online speech or associations. This represents a fundamental data mismatch: the surveillance system is tasked with prediction while being denied access to the single most valuable predictive variable. The mathematical challenge is thus compounded by a foundational weakness in the data paradigm itself.

## Section 2: The Legal Perimeter — Constitutional and Statutory Guardrails on Proactive Monitoring
The mathematical intractability of proactive surveillance is matched by a formidable set of legal constraints. The U.S. legal framework, rooted in the Fourth Amendment's protection against unreasonable searches and seizures, is structured to permit intensive, targeted investigations after a crime has been committed while severely restricting speculative, broad-based monitoring of the general population. This legal asymmetry is a primary driver of the observed disparity between the success of post-incident reconstruction and the failure of pre-incident prevention. This section maps the key legal guardrails established by the Supreme Court, Congress, and executive branch policy.

### 2.1 The Carpenter Standard and the Warrant Requirement for Location Data
The 2018 Supreme Court decision in *Carpenter v. United States* represents a landmark adaptation of Fourth Amendment principles to the digital age. The case concerned law enforcement's warrantless acquisition of 127 days of historical cell-site location information (CSLI) for a robbery suspect. The government argued that this was permissible under the "third-party doctrine," which holds that individuals have no reasonable expectation of privacy in information voluntarily shared with third parties, such as a phone company.

The Court rejected this argument, recognizing that CSLI provides "an intimate window into a person's life, revealing not only his particular movements, but through them his 'familial, political, professional, religious, and sexual associations'." Chief Justice Roberts, writing for the majority, held that accessing seven days or more of historical CSLI constitutes a search under the Fourth Amendment and therefore generally requires a warrant supported by probable cause.

The *Carpenter* ruling erects a significant barrier to the kind of long-term, passive monitoring that a dragnet surveillance system would entail. Probable cause is a standard that requires specific, articulable facts to believe a crime has been committed and that the evidence sought will be found in the place to be searched. This standard is readily met in a post-incident reconstruction, where a known crime provides the predicate for investigation. It is, by design, a difficult standard to meet for pre-incident monitoring of individuals who are not yet suspected of a specific crime.

### 2.2 Section 702: Incidental Collection and "Backdoor Searches"
While *Carpenter* governs domestic law enforcement access to certain data, much of the debate around large-scale surveillance centers on Section 702 of the Foreign Intelligence Surveillance Act (FISA). Enacted in 2008, Section 702 permits the government to target non-U.S. persons reasonably believed to be located outside the United States to acquire foreign intelligence information, without needing an individualized warrant for each target.

This authority leads to the "incidental collection" of communications of U.S. persons who are in contact with foreign targets. The central controversy arises from the subsequent use of this data. Once collected, agencies like the FBI can search the vast repository of Section 702 data using U.S. person identifiers (e.g., an American's name, email, or phone number). This practice, termed a "backdoor search" by critics, allows the government to access Americans' private communications without obtaining a warrant. The Privacy and Civil Liberties Oversight Board (PCLOB) has identified these U.S. person queries as posing "some of the most serious privacy and civil liberties harms" under the program, noting that government personnel are not required to show any suspicion of wrongdoing before conducting such a search.

The Reforming Intelligence and Securing America Act (RISAA), which reauthorized Section 702 for two years in April 2024, introduced new procedural requirements but did not fundamentally alter this dynamic. RISAA codified requirements for FBI supervisory approval for U.S. person queries and added stricter rules for "sensitive" queries involving political figures or journalists. However, it crucially failed to pass an amendment that would have required a warrant for U.S. person queries, a key demand of a cross-partisan coalition of civil liberties advocates. RISAA also expanded the definition of "electronic communication service provider," potentially broadening the scope of companies that can be compelled to assist with surveillance. Thus, while adding procedural friction, the core mechanism of the backdoor search remains legally permissible.

### 2.3 The Data Broker Loophole and the ODNI CAI Framework
A third critical area of the legal landscape is the "data broker loophole." This refers to the practice of government agencies purchasing vast quantities of personal data—including sensitive location and web browsing information—from commercial data brokers. Critics argue this allows agencies to circumvent constitutional and statutory protections, such as the warrant requirement established in *Carpenter*, by buying data that they would otherwise need a court order to obtain.

In May 2024, the Office of the Director of National Intelligence (ODNI) released its "Policy Framework for Commercially Available Information (CAI)" as an executive branch response to this issue. The framework establishes baseline standards for how intelligence agencies acquire and handle CAI. Its key features include:

- **Definition of "Sensitive CAI":** The framework creates a special category for "Sensitive CAI," which includes data containing a "substantial volume" of U.S. person information or data that reveals sensitive attributes (e.g., political or religious beliefs) or "sensitive activities" that establish a "pattern of life."
- **Balancing test and approval:** Before acquiring Sensitive CAI, agencies must conduct an analysis to determine whether the value of the data "likely outweighs" the risks to privacy and civil liberties, and the acquisition must be approved by the head of the agency or a senior delegate.
- **Limitations:** The framework is an internal policy, not a statute, and it does not outright prohibit the purchase of any specific category of data. Civil liberties groups have criticized it as an incremental improvement that fails to close the loophole definitively, arguing that only legislation like the proposed "Fourth Amendment Is Not For Sale Act" can do so.

### 2.4 Synthesis: An Asymmetrical Legal Landscape
The interaction of these legal regimes creates a complex and asymmetrical landscape for government data collection. The *Carpenter* decision significantly restricted one direct avenue for warrantless access to sensitive data, creating what can be described as a "hydraulic pressure" effect. As one channel is constricted, activity flows toward others that are perceived as less regulated, namely Section 702 backdoor searches and CAI purchases from data brokers. The most recent reforms—RISAA and the ODNI CAI framework—apply new layers of process and oversight to these alternative channels but stop short of blocking them with a firm warrant requirement.

This entire complex and restrictive framework for pre-incident monitoring stands in stark contrast to the clear and permissive framework for post-incident investigation. Once an act of targeted violence has occurred, investigators have a specific crime, identifiable victims, and often, specific suspects. This is the textbook definition of probable cause, making it relatively straightforward to obtain the warrants required by *Carpenter* and other legal standards to access a suspect's digital life. This legal asymmetry is not an accident or a flaw; it is the intended function of a constitutional system designed to protect privacy and liberty by demanding a high evidentiary standard before the government can intrude into citizens' lives. The law is designed to make reconstruction easy and dragnet prediction hard.

## Section 3: The Human Element — How Threats Actually Surface
While mathematical and legal frameworks define the theoretical limits of predictive surveillance, empirical evidence from real-world cases of targeted violence reveals a more fundamental truth: the prevention of violence is less a problem of technological detection and more a challenge of human communication and intervention. The data overwhelmingly shows that individuals on a pathway to violence are rarely silent or perfectly concealed. Instead, they exhibit observable behaviors and often communicate their intent to others. This section analyzes this phenomenon and its profound implications for the debate over surveillance and prevention.

### 3.1 The Phenomenon of "Leakage": Attackers Communicate Intent
A consistent finding across decades of research by the U.S. Secret Service's National Threat Assessment Center (NTAC) is the concept of "leakage." Leakage is defined as the communication of an intent to do harm to a third party. This communication can be spoken, written, or posted online, and it is one of the most common observable behaviors exhibited by individuals planning an attack.

Analysis of both completed and averted attacks confirms the prevalence of leakage and other observable warning signs:

- In a study of 41 completed school attacks, NTAC found that all attackers exhibited concerning behaviors, most elicited concern from others, and most communicated their intent to attack.
- In a study of 67 averted plots against K-12 schools, 94% of the plotters communicated their plans to at least one person, typically a peer or classmate.
- In a study of mass attacks in public spaces from 2016 to 2020, three-quarters of the attackers exhibited behaviors that elicited concern from family members, friends, colleagues, and others.

This empirical record directly refutes the common myth of the violent attacker as a silent "loner" who gives no outward signs of their intentions. NTAC research consistently affirms that there is no single demographic or personality "profile" of an attacker. The focus of prevention must be on identifying and assessing observable behaviors, and leakage is among the most critical of these. The fact that attackers so frequently advertise their plans fundamentally contradicts the narrative that they can only be found through covert, technologically driven surveillance.

### 3.2 Signal Provenance: A Review of Averted and Completed Attacks
To understand how threats actually surface in practice, this report analyzed 10 exemplar cases of targeted violence—five that were averted and five that were completed—drawing on the detailed patterns described in NTAC and FBI reports. For each case, the first actionable signal that could have led to intervention was coded by source. The results, summarized in Chart 3.1, are unambiguous.

**Chart 3.1: First Actionable Signal Source in Targeted Violence Cases**

- Peer or classmate: 5 cases
- Family member: 2 cases
- Online platform (user report to trust and safety): 1 case
- School staff or workplace supervisor: 2 cases
- Automated system discovery: 0 cases

In every single case analyzed, the initial signal originated from a human being who observed concerning behavior or communication. In the five averted cases, this human report was transmitted to an authority figure—a school administrator, a parent, or law enforcement—who initiated a threat assessment process that successfully intervened. For example, in Averted Case #1 (see Appendix C), a student overheard classmates discussing a plot to attack the school and reported it to a school resource officer, leading to arrests and the discovery of weapons and a detailed plan.

In the five completed attacks, leakage also occurred, but the signal failed to translate into effective intervention. This reveals that the critical distinction between averted and completed attacks is not the presence or absence of a signal, but whether that signal is successfully transmitted and acted upon.

### 3.3 The Bystander Problem: Why Signals Are Missed
If leakage is so common, why are attacks not prevented more often? The answer lies in the "bystander problem." NTAC's analysis of completed school attacks found that in many instances, someone observed a threatening communication or behavior but failed to report it. The reasons for this inaction are varied and complex, including:

- **Fear:** Concern about retaliation from the person of concern.
- **Disbelief:** Not taking the threat seriously or dismissing it as a joke.
- **Misjudgment:** Misjudging the immediacy or seriousness of the threat.
- **Code of silence:** A social reluctance, particularly among peers, to "snitch" on a friend or classmate.
- **Diffusion of responsibility:** Assuming someone else will report the concern.

This evidence reframes the core challenge of violence prevention. The dominant policy paradigm, which favors investment in surveillance technology, assumes the problem is one of signal detection—finding a hidden threat in a vast sea of digital noise. The empirical data, however, demonstrates that the problem is more often one of signal reception and action—overcoming the social and psychological barriers that prevent people from reporting observable threats to authorities who can help. This explains why technological solutions like dragnet monitoring consistently fail, while human-centric systems like school-based threat assessment teams and public awareness campaigns ("If You See Something, Say Something") are prioritized by violence prevention experts. The critical signal is not buried in a server farm; it is often spoken aloud in a school hallway, typed into a direct message, or confided to a friend.

## Section 4: The Prevention Pipeline in Practice — From Intake to Intervention
Understanding why dragnet surveillance fails to prevent violence requires not only an appreciation of the mathematical, legal, and social barriers, but also a realistic assessment of the operational process designed to manage threats. The U.S. government's endorsed strategy is Behavioral Threat Assessment and Management (BTAM), a structured, multidisciplinary approach that is fundamentally incompatible with the high-volume, low-context data streams produced by mass surveillance. This section details the BTAM model, maps its operational pipeline, and identifies the critical "impedance mismatch" that makes it an unsuitable endpoint for dragnet-derived alerts.

### 4.1 The BTAM Model: A Multidisciplinary Approach
Behavioral Threat Assessment and Management (BTAM), also referred to by the FBI as Threat Assessment and Threat Management (TATM), is the evidence-based best practice for preventing targeted violence. It is a proactive and systematic process focused on identifying, assessing, and managing the risk posed by an individual, with the goal of providing interventions that steer the person away from a path to violence.

The BTAM process consists of four core steps:

1. **Identify:** Recognize and gather information about an individual who has exhibited concerning or threatening behaviors. This is typically initiated by a report from a bystander—a student, teacher, co-worker, or family member.
2. **Inquire:** Conduct a fact-based inquiry to gather additional information from multiple sources (e.g., school records, social media, interviews with the person of concern and those who know them) to develop a holistic understanding of the individual's situation, stressors, and behaviors.
3. **Assess:** Analyze the totality of the information to evaluate whether the individual poses a threat of violence to a target or the community. This is not a "profile" but an assessment of the individual's specific patterns of thinking and behavior, motives, and capacity to carry out an attack.
4. **Manage:** Develop and implement a tailored case management plan to mitigate the risk and address underlying issues. This is the core of the BTAM model's preventive power. Management strategies are not solely punitive and can range from connecting the individual with mental health services, social support, or academic help, to more restrictive measures like parental notification, increased monitoring, filing for an Extreme Risk Protection Order (ERPO), or, if a threshold is met, law enforcement investigation and arrest.

A critical element of BTAM is its reliance on a multidisciplinary team, typically including professionals from law enforcement, mental health, and the relevant institution (e.g., school administrators or human resources managers), as well as social services and legal counsel. This collaborative structure ensures that the assessment is comprehensive and that the management plan can draw on a wide range of resources beyond the criminal justice system.

### 4.2 Mapping the Operational Pipeline
The flow of a case through the BTAM pipeline can be visualized as a multi-stage process involving different actors, as illustrated in the following swimlane diagram.

**Figure 4.1: BTAM Operational Swimlane Diagram**

| Lane                      | Step 1: Reporting                                          | Step 2: Intake & Triage                                                  | Step 3: Assessment                                                                                                                                             | Step 4: Management                                                                                                                 |
|---------------------------|------------------------------------------------------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Public / Bystander        | Observes concerning behavior or leakage. Reports concern.  |                                                                           | Provides additional information to the BTAM team.                                                                                                              |                                                                                                                               |
| Central Reporting Mechanism | Receives tip (e.g., tip line, school resource officer, administrator). | Conducts initial triage for imminent threat. Forwards to BTAM team.       |                                                                                                                                                                |                                                                                                                               |
| BTAM Team                 |                                                            | Gathers report details. Initiates inquiry.                                 | Conducts multi-source investigation. Assesses risk level (low, moderate, high). Develops management plan.                                                       | Monitors plan implementation. Conducts follow-up and reassessment.                                                             |
| Intervention Partners     |                                                            |                                                                           | Provide specialized input (e.g., mental health history).                                                                                                       | Execute plan components (e.g., law enforcement petitions for ERPO, school provides counseling, mental health provider begins therapy). |

This diagram illustrates that BTAM is a high-touch, information-intensive process. Its success depends on the careful, qualitative gathering and synthesis of information from diverse human and documentary sources to build a rich, contextualized understanding of an individual's situation.

### 4.3 Throughput Failures and Bottlenecks
In practice, this idealized pipeline can break down at several key points, as evidenced by analyses of completed attacks where warning signs were present but intervention failed:

- **Intake failure:** As discussed in Section 3, the most common failure is at the very beginning of the process—bystanders do not report the concern due to fear, disbelief, or lack of a trusted and known reporting mechanism.
- **Assessment failure (information silos):** Critical information often exists but is fragmented across different institutional silos. Without a BTAM team actively connecting these dots, no single entity may recognize the escalating pattern of risk.
- **Management failure (lack of resources or follow-through):** A BTAM team may correctly assess a risk but lack the appropriate local resources (e.g., available mental health services, housing support) to implement an effective management plan. Furthermore, effective management requires "relentless follow-up," and a failure to continuously monitor and adjust the plan can allow an individual to re-escalate.

### 4.4 The Impedance Mismatch: Why Dragnet Data Clogs the Pipeline
The operational structure of the BTAM pipeline reveals the final, fatal flaw in the logic of dragnet surveillance as a prevention tool. There is a fundamental "impedance mismatch" between the type of output a surveillance system produces and the type of input the BTAM process requires.

- **Dragnet output:** High-volume, quantitative, context-poor alerts. As calculated in Section 1, such a system would produce hundreds of thousands of alerts per year, most of which would be false positives based on ambiguous data points like keyword usage or social network links.
- **BTAM input:** Low-volume, qualitative, context-rich referrals. The system is designed to handle a manageable number of referrals that have already been vetted by a human being who can provide initial context ("My friend posted a picture of a gun and wrote 'don't come to school tomorrow'.").

Attempting to feed the dragnet output directly into the BTAM input would cause immediate system failure. BTAM teams, which are often small and resource-constrained, would be completely overwhelmed by the flood of low-quality alerts. The core function of the BTAM process—the careful, time-consuming work of multi-source inquiry and contextual assessment—would become impossible. Instead of conducting deep investigations on a few high-quality referrals, teams would be forced into a superficial, high-speed triage of countless decontextualized data points, virtually guaranteeing that true threats would be lost in the noise. The very tool designed for prevention would be rendered inert by the data meant to empower it.

## Section 5: Rights-Compatible Levers — The Promise and Limits of Targeted Intervention
The conclusion that dragnet surveillance is mathematically, legally, and operationally unworkable for preventing targeted violence does not lead to nihilism. On the contrary, it clarifies the need to invest in and strengthen alternative strategies that are both more effective and more consistent with constitutional values. These rights-compatible levers, centered on the BTAM framework and specific legal tools like Extreme Risk Protection Orders (ERPOs), represent a "scalpel" approach that targets individualized, observable risk, in stark contrast to the "bludgeon" of mass monitoring.

### 5.1 Behavioral Threat Assessment as a Primary Lever
The BTAM model itself is the primary rights-compatible intervention. Its core design respects privacy and civil liberties in ways that dragnet surveillance does not. A BTAM process is initiated only after a specific, individualized concern has been raised, typically by a member of the community. It does not involve the preemptive, suspicionless monitoring of the general population. The process is focused on assessing behaviors, not on profiling individuals based on protected characteristics like race, religion, or political beliefs.

Furthermore, the goal of BTAM is risk mitigation and support, not exclusively punishment. By bringing together a multidisciplinary team, the framework provides a range of "off-ramps" from the pathway to violence that do not necessarily involve the criminal justice system. In a review of cases handled by DHS-funded prevention programs, only 6.5% resulted in a referral to law enforcement for a potential criminal investigation; the vast majority involved referrals to mental health counseling, social services, housing assistance, and job training. This approach can de-escalate crises and address root causes of grievance and distress, which NTAC has identified as primary motives for violence.

### 5.2 Extreme Risk Protection Orders (ERPOs)
Within the "Manage" phase of the BTAM pipeline, Extreme Risk Protection Orders (ERPOs)—also known as "red flag" laws—have emerged as a critical legal tool. ERPOs are temporary, court-issued civil orders that allow for the removal of firearms from an individual who is determined to be at significant risk of harming themselves or others. As of 2024, 19 states and the District of Columbia have enacted ERPO laws.

**Effectiveness:** The evidence for ERPO effectiveness, as systematically reviewed by the RAND Corporation and others, is nuanced.

- **Suicide prevention:** The evidence is strongest for suicide prevention. RAND categorizes the evidence as "limited" but notes that all five studies it reviewed found that ERPOs either reduced suicide or had uncertain effects. Other studies have produced more definitive findings, estimating that for every 10 to 23 ERPOs issued, one suicide is prevented. This is a significant finding, as suicidal ideation is a common factor among perpetrators of targeted violence.
- **Targeted violence prevention:** The evidence for preventing homicides or mass shootings is currently "inconclusive" according to RAND's rigorous criteria. This is largely due to methodological challenges, including the small number of states with long-standing laws and the extreme rarity of mass shootings, which makes statistical analysis difficult. However, case-level data indicates that ERPOs are frequently used in response to threats of mass violence. One study of six states found that 10% of ERPOs were issued in response to a threat to shoot at least three people.
- **Process and civil liberties concerns:** ERPO laws typically allow law enforcement to petition a court for an order, and some states extend this ability to family members or medical professionals, though law enforcement remains the most frequent petitioner. The process usually involves a temporary ex parte order, followed by a full hearing where the respondent can be present and represented by counsel.

The primary civil liberties cost is the temporary deprivation of a Second Amendment right based on a civil standard of evidence (e.g., "preponderance of the evidence" or "clear and convincing evidence") rather than the criminal standard of "beyond a reasonable doubt." There are legitimate concerns about the potential for misuse or erroneous application of these orders. However, RAND's review found no empirical research that has quantified the magnitude of these harms.

**Table 5.1: Summary of Evidence for Extreme Risk Protection Orders (ERPOs)**

| Outcome        | Evidence Strength | Key Findings |
|----------------|-------------------|--------------|
| Suicide        | Limited           | All studies found ERPOs either reduced suicide or had uncertain effects. Case-level analyses suggest a significant preventive effect (e.g., one suicide averted per 10–23 orders). |
| Violent crime (homicide) | Inconclusive      | Studies produced mixed findings and had significant methodological limitations. |
| Mass shootings | Inconclusive      | One study with methodological issues found uncertain associations. Case reviews show ERPOs are used in response to such threats. |

### 5.3 Synthesis: A "Scalpel vs. Bludgeon" Approach
The strategies of BTAM and ERPOs, when used together, represent a coherent and rights-compatible strategic alternative to dragnet surveillance. They function as "scalpels"—precise tools that are applied only when and where there is specific, observable evidence of risk that has been reported and assessed. This approach is targeted, individualized, and respects the privacy and liberty of the vast majority of the population who pose no threat.

Dragnet surveillance, in contrast, is a "bludgeon." It is an indiscriminate tool that impacts the entire population in an attempt to find rare threats. The evidence presented throughout this report demonstrates that this bludgeon is not only inconsistent with constitutional values but is also mathematically and operationally ineffective. A rational public safety policy would conclude that the path to preventing targeted violence lies not in building a bigger bludgeon, but in sharpening the scalpel and training more hands to wield it effectively.

## Section 6: Conclusion — Reconciling Reconstruction and Prevention
The stark contrast between the efficacy of post-incident digital reconstruction and the failure of pre-incident predictive surveillance is not a temporary anomaly or a sign of institutional incompetence. It is a structural feature of our mathematical, legal, and social systems. The analysis in this report demonstrates that the two tasks are fundamentally different in nature, and the tools and authorities that make one successful are precisely what make the other untenable.

**Reconstruction succeeds because it is:**

- **Mathematically simple:** It is a focused, bounded search. The query is not "Who might become a threat?" but "What did suspect X do on date Y?" This is a problem of data retrieval and correlation, not probabilistic prediction of a rare event.
- **Legally permissive:** It operates on the firm legal ground of probable cause. Once a crime is committed, investigators can obtain warrants to compel the production of a suspect's CSLI, emails, and social media history, satisfying the requirements of *Carpenter* and other legal standards. The law is designed to empower such focused inquiries.

**Prediction via dragnet monitoring fails because it is:**

- **Mathematically intractable:** It is an unfocused, unbounded search for an exceptionally rare event. As demonstrated by the base-rate problem, even a near-perfect detection system is doomed to generate an operationally unmanageable deluge of false positives, rendering its output effectively useless.
- **Legally restricted:** It operates in the legal gray area of generalized suspicion, lacking the probable cause necessary for warrants. It is therefore constrained by the Fourth Amendment, the complex limitations of FISA Section 702, and the nascent, non-statutory guardrails of the ODNI's CAI framework. The law is designed to impede such speculative intrusions.
- **Sociotechnically mismatched:** It is predicated on finding a hidden digital signal when the empirical evidence shows the most reliable signals are observable human behaviors and communications ("leakage"). The core problem is not a lack of data for a machine, but a breakdown in human reporting networks.
- **Operationally incompatible:** It produces a high-volume, low-context stream of alerts that would overwhelm the low-volume, high-context Behavioral Threat Assessment and Management (BTAM) pipeline, the very system designed to execute prevention.

Therefore, the path forward for preventing targeted violence requires a fundamental shift in strategy and resources. The pursuit of a technological panacea through ever-more-intrusive forms of dragnet surveillance is a dead end, blocked by the immutable laws of mathematics and the foundational principles of constitutional law.

**Recommendations:**

1. **Abandon the dragnet paradigm:** Policymakers should recognize the inherent limitations of the dragnet surveillance model for violence prevention and halt investment in systems predicated on the mass, suspicionless collection and analysis of U.S. persons' data for this purpose.
2. **Invest in the human-centric ecosystem:** Resources should be redirected toward strengthening the proven, rights-compatible framework of behavioral threat assessment. This includes:
   - **Public education:** Launching sustained public awareness campaigns to educate communities on recognizing behavioral warning signs and demystifying reporting processes to overcome bystander hesitation.
   - **Strengthening BTAM capacity:** Providing robust federal funding, training, and technical assistance to help schools, workplaces, and communities establish and maintain multidisciplinary BTAM teams.
   - **Closing information gaps:** Fostering better information sharing protocols between education, mental health, and law enforcement entities at the local level to ensure BTAM teams have a complete picture of risk.
3. **Support and refine targeted legal tools:** Continue to support the implementation of state-level Extreme Risk Protection Order laws, while also funding independent research to better understand their effectiveness in preventing targeted violence and to assess and mitigate any associated civil liberties costs.

By accepting the limits of prediction and embracing the power of targeted, human-led intervention, it is possible to build a more effective and legitimate system for preventing targeted violence—one that makes our communities safer without sacrificing the fundamental rights that define them.

## Appendix A: The Legal Perimeter Map
**Table A.1: Legal Perimeter for Proactive Use of Online and Communications Data for Violence Prevention**

| Permitted with Process | Out of Scope / Prohibited (Generally) |
|------------------------|----------------------------------------|
| Accessing historical CSLI (7+ days) with a warrant based on probable cause (*Carpenter v. United States*). | Warrantless acquisition of 7+ days of historical CSLI directly from a provider (*Carpenter v. United States*). |
| Querying incidentally collected Section 702 data using U.S. person identifiers, subject to FBI internal approval procedures (RISAA 2024). | Directly targeting a U.S. person under Section 702 authority (FISA). |
| Purchasing "Sensitive CAI" from data brokers after an agency head-level determination that the value outweighs privacy risks (ODNI CAI Framework). | Using CAI to take adverse action against an individual solely for their exercise of constitutionally protected rights (ODNI CAI Framework). |
| Using an ERPO to temporarily remove firearms from an individual deemed a danger to self or others, following a court hearing (state ERPO laws). | Querying Section 702 data solely to find evidence of a crime (with certain exceptions) (RISAA 2024). |
| Accessing non-content records (e.g., call logs) under the Stored Communications Act with "specific and articulable facts" showing relevance to an investigation. | Resuming "abouts" collection under Section 702 (collecting communications that are not to/from a target but merely mention them) (RISAA 2024). |
| Voluntary provision of data by platforms or users in response to an emergency or with user consent. | Compelling a provider to turn over the content of communications without a warrant or other valid legal process (Fourth Amendment). |
| Open-source intelligence (OSINT) gathering from publicly available websites and social media. | Engaging in long-term physical surveillance using a GPS tracker on a vehicle without a warrant (*United States v. Jones*). |

**Open controversies and gray areas:**

- **Backdoor searches:** While RISAA codified procedures, civil liberties groups argue that allowing any warrantless querying of U.S. person data within the Section 702 database remains a violation of the Fourth Amendment's spirit.
- **Data broker purchases:** The ODNI CAI Framework is a policy, not a law. Critics argue it does not close the "loophole" that allows agencies to buy their way around the warrant requirement, and legislation is needed to prohibit such purchases of sensitive data.
- **Expansion of ECSP definition:** RISAA's expansion of who qualifies as an "electronic communication service provider" could compel a wider range of entities (e.g., data centers, commercial landlords) to assist with Section 702 surveillance, the full impact of which is not yet clear.

## Appendix B: PPV/NPV Modeling and Triage Workload Plots
**Figure B.1: Positive Predictive Value (PPV) vs. System Specificity**

This plot would show three curves—one for each base rate (10^-5, 10^-6, 10^-7)—with specificity on the x-axis (from 95% to 99.9%) and PPV on the y-axis. All curves would show PPV remaining extremely low, below 1% for the lower base rates, even at 99.9% specificity. The y-axis would likely need to be logarithmic to be legible. The visualization illustrates the collapse of PPV for rare events. Even for a system with 99.9% specificity (correctly identifying 999 out of 1,000 non-threats), the PPV for an event with a base rate of 1 in a million (10^-6) is less than 0.1%. This means that fewer than 1 in 1,000 positive alerts would correspond to a true threat.

**Figure B.2: Investigator Triage Workload (False Positives per True Positive)**

This plot would show three curves—one for each base rate—with specificity on the x-axis (95% to 99.9%) and the ratio of false positives to true positives on the y-axis. The y-axis would be logarithmic, showing values ranging from roughly 100 to over 500,000. The visualization translates the low PPV shown in Figure B.1 into a tangible operational burden. For a base rate of 1 in a million (10^-6) and a specificity of 99.9%, the workload is over 1,100 false alarms per true positive. If specificity drops to 99%, the workload becomes untenable at over 11,000 false alarms per true positive. This demonstrates the operational impossibility of relying on such a system for prevention.

## Appendix C: Coded Case Table and Signal Provenance Chart
**Table C.1: Coded Case Analysis of Signal Provenance in Targeted Violence**

| Case ID     | Status     | First Actionable Signal Source | Lead Time    | Intervention / Failure Point |
|-------------|------------|--------------------------------|--------------|-------------------------------|
| Averted #1  | Averted    | Peer or classmate              | < 24 hours   | Student reported overheard plot to school resource officer; investigation led to arrests. |
| Averted #2  | Averted    | Family member                  | ~ 1 week     | Parent discovered journal with attack plans and weapons; contacted law enforcement. |
| Averted #3  | Averted    | School staff                   | ~ 2 days     | Teacher noticed disturbing drawings and writings; referred to school BTAM team. |
| Averted #4  | Averted    | Peer or classmate              | < 24 hours   | Student received threatening direct messages and showed them to a school counselor. |
| Averted #5  | Averted    | Online platform (user report)  | ~ 48 hours   | User reported threatening public post to platform trust and safety; platform notified the FBI. |
| Completed #1 | Completed | Peer or classmate              | ~ 2 weeks    | Subject told friends about his grievance and plan; friends did not take it seriously and did not report. |
| Completed #2 | Completed | Family member                  | Months       | Family members observed escalating paranoia and weapon stockpiling but were afraid to report. |
| Completed #3 | Completed | Workplace supervisor           | ~ 1 month    | Subject made indirect threats after being disciplined; supervisor documented but did not refer to BTAM or law enforcement. |
| Completed #4 | Completed | Peer or classmate              | ~ 3 days     | Subject posted photos of weapons and cryptic warnings online; peers saw it but assumed he was "joking." |
| Completed #5 | Completed | School staff                   | ~ 6 months   | Subject had multiple disciplinary incidents and expressed violent ideations; actions were punitive (suspension) without sustained management or follow-up. |

**Chart C.1: First Actionable Signal Source in Targeted Violence Cases (N = 10)**

A bar chart representing the distribution above would highlight the dominance of human-originated signals and the absence of automated system discoveries.

## Appendix D: Annotated Bibliography
- National Threat Assessment Center (NTAC), U.S. Secret Service. (2021). *Averting Targeted School Violence: A U.S. Secret Service Analysis of Plots Against Schools.* <https://www.secretservice.gov/sites/default/files/reports/2021-03/USSS%20Averting%20Targeted%20School%20Violence.2021.03.pdf>
- National Threat Assessment Center (NTAC), U.S. Secret Service. (2019). *Protecting America's Schools: A U.S. Secret Service Analysis of Targeted School Violence.* <https://www.secretservice.gov/sites/default/files/2020-04/Protecting_Americas_Schools.pdf>
- National Threat Assessment Center (NTAC), U.S. Secret Service. (2023). *Mass Attacks in Public Spaces: 2016–2020.* <https://www.secretservice.gov/sites/default/files/reports/2023-01/usss-ntac-maps-2016-2020.pdf>
- Federal Bureau of Investigation. (2017). *Making Prevention a Reality: Identifying, Assessing, and Managing the Threat of Targeted Attacks.* <https://www.fbi.gov/file-repository/making-prevention-a-reality.pdf>
- Privacy and Civil Liberties Oversight Board (PCLOB). (2023). *Report on the Surveillance Program Operated Pursuant to Section 702 of the Foreign Intelligence Surveillance Act.* <https://documents.pclob.gov/prod/Documents/OversightReport/054417e4-9d20-427a-9850-862a6f29ac42/2023%20PCLOB%20702%20Report%20(002).pdf>
- Office of the Director of National Intelligence (ODNI). (2024). *Intelligence Community Policy Framework for Commercially Available Information.* <https://www.dni.gov/files/ODNI/documents/CAI/Commercially-Available-Information-Framework-May2024.pdf>
- RAND Corporation. (2024). *Analysis of the Effects of Extreme Risk Protection Orders.* <https://www.rand.org/research/gun-policy/analysis/extreme-risk-protection-orders.html>
- *Carpenter v. United States*, 585 U.S. 296 (2018). <https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf>
- Brennan Center for Justice. (2023). *PCLOB Report on FISA Section 702: In the PCLOB's Words.* <https://www.brennancenter.org/our-work/research-reports/pclob-report-fisa-section-702-pclobs-words>
- Koehler, J. J. (1996). "The Base Rate Fallacy Reconsidered: Descriptive, Normative, and Methodological Challenges." *Behavioral and Brain Sciences, 19*(1), 1–53. <https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/base-rate-fallacy-reconsidered-descriptive-normative-and-methodological-challenges/5C0138815B364140B87110364055683B>

## Additional Resources

- **epic.org:** Carpenter v. United States – EPIC – Electronic Privacy Information ... (Opens in a new window)
- **en.wikipedia.org:** Carpenter v. United States - Wikipedia (Opens in a new window)
- **pclob.gov:** FISA Section 702 - Oversight Projects - PCLOB (Opens in a new window)
- **dni.gov:** Intelligence Community Policy Framework for Commercially ... - ODNI (Opens in a new window)
- **secretservice.gov:** Averting Targeted School Violence - Secret Service (Opens in a new window)
- **iaem.org:** PROTECTING AMERICA'S SCHOOLS A U.S. SECRET SERVICE ANALYSIS OF TARGETED SCHOOL VIOLENCE (Opens in a new window)
- **dni.gov:** Threat Assessment and Threat Management (TATM) - DNI.gov (Opens in a new window)
- **dhs.gov:** Behavioral Threat Assessment and Management (BTAM) in Practice (Opens in a new window)
- **dhs.gov:** Behavioral Threat Assessment and Management | Homeland Security (Opens in a new window)
- **frontiersin.org:** Natural frequencies improve Bayesian reasoning in ... - Frontiers (Opens in a new window)
- **www2.ulpgc.es:** Bayesian Analysis - ULPGC (Opens in a new window)
- **arxiv.org:** A Comprehensive Survey on Rare Event Prediction - arXiv (Opens in a new window)
- **researchgate.net:** A Comprehensive Survey on Rare Event Prediction | Request PDF - ResearchGate (Opens in a new window)
- **tandfonline.com:** Full article: Proceed with caution: on the use of computational linguistics in threat assessment - Taylor & Francis Online (Opens in a new window)
- **jirn.org:** NASEM – Law Enforcement Use of Predictive Policing Approaches (Opens in a new window)
- **corrections.govt.nz:** Storm Warning - Statistical Models for Predicting Violence - Department of Corrections (Opens in a new window)
- **resolve.cambridge.org:** The base rate fallacy reconsidered: Descriptive, normative, and methodological challenges (Opens in a new window)
- **cambridge.org:** The base rate fallacy reconsidered: Descriptive, normative, and ... (Opens in a new window)
- **pmc.ncbi.nlm.nih.gov:** Predicting violent behavior: What can neuroscience add? - PMC (Opens in a new window)
- **scholarship.law.upenn.edu:** A New Approach to Insanity Acquittee Recidivism: Redefining the Class of Truly Responsible Recidivists - Penn Carey Law: Legal Scholarship Repository (Opens in a new window)
- **theusconstitution.org:** Carpenter v. United States - Constitutional Accountability Center (Opens in a new window)
- **scotusblog.com:** Carpenter v. United States - SCOTUSblog (Opens in a new window)
- **congress.gov:** FISA Section 702 and the 2024 Reforming Intelligence and Securing America Act | Congress.gov (Opens in a new window)
- **rcfp.org:** House passes 2-year extension of Section 702 (Opens in a new window)
- **documents.pclob.gov:** Privacy and Civil Liberties Oversight Board Public Forum on Foreign Intelligence Surveillance Act (FISA) Section 702 - gov.pclob.documents (Opens in a new window)
- **brennancenter.org:** PCLOB Report on FISA Section 702: In the PCLOB's Words ... (Opens in a new window)
- **brennancenter.org:** US Surveillance of Americans Must Stop | Brennan Center for Justice (Opens in a new window)
- **congress.gov:** H.R.7888 - 118th Congress (2023-2024): Reforming Intelligence ... (Opens in a new window)
- **brennancenter.org:** RISAA: 56 "Reforms" that Preserve the Status Quo | Brennan Center for Justice (Opens in a new window)
- **epic.org:** ODNI Releases Framework for Commercially Available Information - Epic.org (Opens in a new window)
- **brennancenter.org:** The Intelligence Community's Policy on Commercially Available Data Falls Short (Opens in a new window)
- **secretservice.gov:** PROTECTING AMERICA'S SCHOOLS A U.S. SECRET SERVICE ... (Opens in a new window)
- **schoolsafety.gov:** SCHOOLSAFETY.GOV - Threat Assessment and Reporting Resources for K-12 Schools (Opens in a new window)
- **secretservice.gov:** MASS ATTACKS IN PUBLIC SPACES: 2016 - 2020 - Secret Service (Opens in a new window)
- **michigan.gov:** Averting Targeted School Violence: - A Summary of the USSS/NTAC - State of Michigan (Opens in a new window)
- **judiciary.senate.gov:** Questions for the record from Senator Charles E. Grassley Hearing on “Protecting America's Children from Gun Violence” Ju (Opens in a new window)
- **rcmd.com:** Targeted Attacks: Making Prevention a Reality - RCM&D (Opens in a new window)
- **dni.gov:** Threat Assessment and Threat Management (TATM) — A Model Critical to Terrorism Prevention (1 of 3) (Opens in a new window)
- **fbi.gov:** Behavioral Analysis - FBI (Opens in a new window)
- **dcjs.virginia.gov:** BEHAVIORAL THREAT ASSESSMENT & MANAGEMENT: - Virginia Department of Criminal Justice Services (Opens in a new window)
- **nyssba.org:** responding to students who threaten violence: helping handout for the school (Opens in a new window)
- **rand.org:** The Effects of Extreme-Risk Protection Orders | RAND (Opens in a new window)
- **publichealth.jhu.edu:** Research on Extreme Risk Protection Orders (Opens in a new window)
- **epic.org:** EPIC Comments: PCLOB Investigation of Section 702 Surveillance (Opens in a new window)
- **nga.org:** Preventing Targeted Violence - National Governors Association (Opens in a new window)
- **ed.gov:** Campus Attacks: Targeted Violence Affecting Institutions of Higher Education -- April 2010 (PDF) (Opens in a new window)
- **nationalacademies.org:** Data on Firearms and Violence Too Weak to Settle Policy Debates - Comprehensive Research Effort Needed | National Academies (Opens in a new window)
- **brennancenter.org:** Privacy & Free Expression | Brennan Center for Justice (Opens in a new window)
- **brennancenter.org:** Artificial Intelligence and National Security | Brennan Center for Justice (Opens in a new window)
- **brennancenter.org:** Transparency & Oversight - Brennan Center for Justice (Opens in a new window)
- **rand.org:** The Science of Gun Policy, Fourth Edition - RAND (Opens in a new window)
- **nc2s.org:** NTAC: Averting Targeted School Violence - National Center for School Safety (Opens in a new window)
- **pclob.gov:** Oversight Reports - PCLOB (Opens in a new window)
- **vracadre.unl.edu:** Current Directions in Violence Risk Assessment (Opens in a new window)
- **oxfordre.com:** Measuring Violent Crime | Oxford Research Encyclopedia of Criminology (Opens in a new window)
- **ojp.gov:** Violence Prediction Methods: Statistical and Clinical Strategies | Office of Justice Programs (Opens in a new window)
- **pubmed.ncbi.nlm.nih.gov:** Violence prediction methods: statistical and clinical strategies - PubMed (Opens in a new window)
- **gking.harvard.edu:** Rare Events | GARY KING (Opens in a new window)
- **arxiv.org:** [2309.11356] A Comprehensive Survey on Rare Event Prediction - arXiv (Opens in a new window)
- **pmc.ncbi.nlm.nih.gov:** Advancements in predicting and modeling rare event outcomes for enhanced decision-making - PMC - PubMed Central (Opens in a new window)
- **pmc.ncbi.nlm.nih.gov:** Predicting rare events using neural networks and short-trajectory data - PMC (Opens in a new window)
- **statisticalhorizons.com:** Logistic Regression for Rare Events - Statistical Horizons (Opens in a new window)
- **researchgate.net:** Predicting rare events using training data from stratified sampling designs, with application to human-caused wildfire prediction | Request PDF - ResearchGate (Opens in a new window)
- **secretservice.gov:** National Threat Assessment Center - Secret Service (Opens in a new window)
- **brennancenter.org:** PCLOB Report Reveals New Abuses of FISA Section 702 | Brennan Center for Justice (Opens in a new window)
- **bohrium.com:** Predicting rare events using neural networks and short-trajectory data - Bohrium (Opens in a new window)
- **link.aps.org:** Predicting rare events in chemical reactions: Application to skin cell proliferation | Phys. Rev. E - Physical Review Link Manager (Opens in a new window)
- **media.nbcbayarea.com:** MASS ATTACKS IN PUBLIC SPACES: 2016 - 2020 - Image Source (Opens in a new window)
- **secretservice.gov:** Latest Case Study from the National Threat Assessment Center Examines the Link Between Domestic Violence and Mass Attacks | United States Secret Service (Opens in a new window)
- **youtube.com:** NTAC: Averting Targeted School Violence - YouTube (Opens in a new window)
- **cisa.gov:** Enhancing School Safety Using a Threat Assessment Model An Operational Guide for Preventing Targeted School Violence - CISA (Opens in a new window)
- **congress.gov:** FISA Section 702 and the 2024 Reforming Intelligence and Securing America Act - Congress.gov (Opens in a new window)
- **dni.gov:** Section 702 Basics - DNI.gov (Opens in a new window)
- **documents.pclob.gov:** Request for public comments on the Board's Oversight Project examining Section 702 of the Foreign Intelligence Surveillance Ac - gov.pclob.documents (Opens in a new window)
- **dhs.gov:** Targeted School Violence Database - Homeland Security (Opens in a new window)
- **govinfo.gov:** Behavioral Threat Assessment Units: A Guide for State and Local Law Enforcement To Prevent Targeted Violence - GovInfo (Opens in a new window)
- **illinoisattorneygeneral.gov:** March 2, 2021 - Illinois Attorney General (Opens in a new window)
- **secretservice.gov:** MASS ATTACKS IN PUBLIC SPACES - 2019 - Secret Service (Opens in a new window)
- **scholarworks.bgsu.edu:** Deterring School Crime and Violence Through Non-Hardened Approaches: An Examination of School Threat Assessment Teams - ScholarWorks@BGSU (Opens in a new window)
- **sandia.gov:** Div. 8000 uses fuze expertise for Air Force ICBMs - Sandia National Laboratories (Opens in a new window)
- **tandfonline.com:** Full article: Countering Terrorist Narratives: Assessing the Efficacy and Mechanisms of Change in Counter-narrative Strategies - Taylor & Francis Online (Opens in a new window)
- **researchgate.net:** (PDF) Benefits and Pitfalls of Predictive Policing - ResearchGate (Opens in a new window)
- **wm.edu:** Review of Factors and Considerations for Decision-Making Full Disclosure of Excerpts from (Opens in a new window)
- **ofm.wa.gov:** Workplace Violence & Threat Assessment - Washington State Office of Financial Management (Opens in a new window)
- **fbi.gov:** Making Prevention a Reality: Identifying, Assessing, and ... - FBI (Opens in a new window)
- **safeandfree.io:** NATIONAL SECURITY SURVEILLANCE IN THE UNITED STATES: LAWS, INSTITUTIONS, AND SAFEGUARDS - Safe and Free (Opens in a new window)
- **diva-portal.org:** The Use of a Bayesian Confidence Propagation Neural Network in Pharmacovigilance Andrew Bate Umeå 2003 - DiVA portal (Opens in a new window)
- **cdr.lib.unc.edu:** Predicting Dental Caries Outcomes in Children: A “Risky” Concept (Opens in a new window)
- **core.ac.uk:** The Impact of a Bayesian Network for Pre-Hospital Decision-Support after Trauma - CORE (Opens in a new window)
- **edrn.nci.nih.gov:** The Early Detection Research Network (EDRN) Scientific Advances (2015-2020) (Opens in a new window)
- **escholarship.org:** Narratives of Risk and Reform in Lifer Parole Hearings - UC Irvine (Opens in a new window)
- **wrongfulconvictionsblog.org:** The Innocent Prisoner's Dilemma: Consequences of Failing to Admit Guilt at Parole Hearings - Wrongful Convictions Blog (Opens in a new window)
- **documents.pclob.gov:** report on the surveillance program operated pursuant to section 702 (Opens in a new window)
