## Bad Smells in Industrial Automation: Sniffing out Feature Envy

Authors: Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; distributed control system; CPS; CPPS; design smell; code smell; bad smell; anti-pattern; Feature Envy; metric; measure; Production systems; Automation; Maintenance engineering; Software systems; Feature extraction; Control systems; IEC Standards

Abstract: Bad Smells are sub-optimal software structures or patterns. They can obstruct the understandability of a software system and cause maintenance issues. As a result, it is critical to avoid Bad Smells. While the subject is well-researched in software engineering, it remains an unresolved issue in industrial automation, e.g., when developing control software in the context of a Cyber-Physical Production System (CPPS). In this short paper, we present possible detection methods for Feature Envy, a smell that indicates bad modularization of a software system. We explain how these methods can be applied to analyze control software developed in IEC 61499. We present first results as well as next steps.

Publication: 2022 48th Euromicro Conference on Software Engineering and Advanced Applications (SEAA)

Year: 2022

ISSN:

ISBN: 978-1-6654-6153-5

DOI: 10.1109/SEAA56994.2022.00061

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10011523

Publisher: IEEE

## IEC 61499 Skill-based Distributed Design Pattern

Authors: Lisa Sonnleithner; Anna-Lena Hager; Alois Zoitl; Kristof Meixner

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL SQI ISE, TU Vienna, Vienna, Austria

Keywords: IEC 61499; Distributed control system; Software design; Software architecture; Design pattern; Skill; Production systems; Flowcharts; Mechatronics; Software; Hardware; Manufacturing; Behavioral sciences

Abstract: Cyber-physical production systems (CPPSs) are modern production systems that aim to integrate the latest techniques and technologies from IT to enable flexible/adaptive manufacturing. The IEC 61499 standardizes a domain-specific modeling language used for developing control software for distributed CPPSs. However, currently, IEC 61499 software misses concrete design guidelines, and those that exist are often not concrete enough to implement high-quality software, which makes changeability and refactoring error-prone and tedious. Furthermore, modularization and decoupling of hardware access and software functions are missing concrete design patterns. This paper aims to implement and test the concepts of skill-based design patterns for IEC 61499 for a concrete use case in a simulation. We employ a case study to demonstrate the approach’s feasibility, achieve the benefits of modularity, adaptability, and maintainability, and facilitate better error handling.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275380

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275380

Publisher: IEEE

## Complexity of Structured Text in IEC 61499 Function Blocks: A Survey.

Authors: Lisa Sonnleithner; Bianca Wiesmayr; Antonio Manuel Gutiérrez; Rick Rabiser; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Distributed Control System; CPS; CPPS; Metric; Measure; Measurement; Surveys; Production systems; Codes; Software; Complexity theory; DSL

Abstract: The rising complexity of modern production systems raises the need for evaluating the code quality also in control software engineering. Complexity metrics can help identifying code that is difficult to maintain and may benefit from a refactoring. Although complexity metrics have already been adapted to the domain-specific languages (DSLs) used for cyber-physical production systems (CPPSs), literature on whether developers benefit from using these metrics is limited. Also, the complexity perception of code by the domain experts remains to be investigated. The perceived difficulty of comprehending a program can vary among developers and also between different implementation variants of the same functionality. We therefore asked industrial experts, who have experience in the respective DSLs, to rate the complexity of semantically equivalent implementations to find out which metric best represents their complexity perception and whether there are differences between implementation variants. The examples used in the study were inspired, in parts, by an open source library for IEC 61131-3. We found that the Cognitive Complexity metric is a useful representation of the software complexity in the domain, as it best matched the domain experts’ perception of complexity. These metrics should therefore be supported by the analysis tools.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275434

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275434

Publisher: IEEE

## Bad Smells in IEC 61499-based Control Software: Sniffing out Shotgun Surgery

Authors: Dunja Životin; Lisa Sonnleithner; Alois Zoitl

Author Affiliations: CDL VaSiCS, Johannes Kepler University, Linz, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria

Keywords: IEC 61499; Bad Smells; Shotgun Surgery; Computer languages; Codes; Surgery; Market research; Software; IEC Standards; Manufacturing automation

Abstract: Bad smells are code patterns which have a negative influence on software, often impacting its quality and maintainability. Because of these negative effects, it is important to detect and avoid them. In the domain of software engineering, the topic of bad smells has been widely researched. On the other hand, in the area of industrial automation and PLC programming languages, bad smells have not received the same amount of attention. Shotgun Surgery is a code smell which we can find when a functionality is used in a certain number of places in code. It starts smelling when every change to the functionality requires many smaller changes to the places where it’s used. If we take a closer look at Shotgun Surgery in the domain of IEC 61499, we see that the general trend persists and that there is no adequate research done on it. In this paper, we want to identify Shotgun Surgery scenarios and showcase multiple existing and new approaches for its detection in IEC 61499.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275499

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275499

Publisher: IEEE

## Using Tool Support to Visualize and Interact with IEC 61499 Control Software

Authors: Philipp Bauer; Lisa Sonnleithner; Elene Kutsia; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; control software; software visualization; tool demo; Measurement; Industries; Visualization; Maintenance engineering; Software; IEC Standards; Manufacturing automation

Abstract: The field of industrial automation has witnessed a significant increase in software development and maintenance efforts in recent years. This can be attributed to the demand for shorter product life cycles and customized products, leading to increasingly complex applications. As a result, control software engineers are facing new challenges. In this paper, we present our tool for visualizing industrial automation software. It provides engineers with a unique perspective on their large-scale applications. The tool offers several benefits, including convenient tracing of control and information flow across multiple levels of hierarchy, applying metrics to the visualization, and various interaction methods. The tool is tightly integrated into an existing IDE, providing a unique workflow for software analysis and maintenance. We discuss the experiences of engineers of our industry partner, who have been using the tool, and next steps.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275595

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275595

Publisher: IEEE

## Clone Detection in IEC 61499 using Metainformation

Authors: Elene Kutsia; Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; control software; clone detection; duplicated code; code smell; Manufacturing industries; Codes; Computer bugs; Cloning; Maintenance engineering; Software; IEC Standards

Abstract: Analyzing and maintaining the quality of control software is pivotal in the plant manufacturing industry. During software development, certain negative patterns frequently occur. These negative patterns are called code smells and are characterized by code that is hard to understand, maintain or expand. One such smell is duplicated code, also known as clones. Clones often result from clone-and-own reuse, which is common in practice. Detecting clones is crucial to avoid bug propagation and keep maintenance efforts low. This work deals with detecting clones in control software written in the domain-specific modeling language IEC 61499.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275611

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275611

Publisher: IEEE

## Using Graph Clustering Algorithms to Modularize IEC 61499 Control Software

Authors: Philipp Bauer; Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 614499; control software; clustering algorithms; code smells; modularization; coupling; cohesion; Couplings; Software maintenance; Codes; Industrial control; Software algorithms; Semantics; Clustering algorithms

Abstract: Software size and complexity in all kinds of domains increase rapidly in recent times, making software maintenance and reusability increasingly difficult. Analysis of existing software and subsequent re-modularization can help with these challenges. Although software re-modularization can be time- and resource-intensive, it can support engineers in improving the quality of their systems in the future. Code can contain certain patterns, such as code smells, that define some kind of problematic implementation that is usually inefficient and hinders future development. We explore the use of a semantic clustering algorithm, which aims to minimize the code smell "Feature Envy". We apply this algorithm recursively to create a multi-level hierarchy. With this approach, we explore the re-modularization of existing IEC 61499 control systems. First tests we conducted on example implementations of a capping station and a real-life-sized industrial control system show a significant reduction of Feature Envy and thus the coupling between modules using this approach.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275726

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275726

Publisher: IEEE

## Variability-Driven Knowledge Discovery in IEC 61499 Systems

Authors: Anna-Lena Hager; Shubham Sharma; Lisa Sonnleithner

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, Linz, Austria; CDL VaSiCS, Linz, Austria

Keywords: IEC 61499; Distributed control system; Unsupervised Machine Learning; Variability Mining; Dimensionality reduction; Knowledge discovery; Software; Maintenance; IEC Standards; Interviews; Information technology; Standards; Manufacturing automation; Manufacturing systems

Abstract: Cyber-physical production systems (CPPSs) are advanced manufacturing systems that integrate the latest information technology techniques to enable flexible and adaptive production processes. The IEC 61499 standard defines a domain-specific modeling language for developing control software for distributed CPPSs. In CPPS, as well as in other domains, variability must be managed. However, effective management first requires the identification and extraction of this variability. Thus, this paper aims to explore and implement machine learning-based Knowledge Discovery techniques within the IEC 61499 standard. By employing a first case study, we demonstrate how to extract variability in IEC 61499-based applications. Our approach leverages techniques such as Term Frequency Inverse Document Frequency (TF-IDF) vectorization and cosine similarity to identify and cluster variations in software components. In the future, we plan to apply this approach to a greater scope of the IEC 61499 standard and develop evaluation methods to validate and improve our methodology. From the first results, integrating machine learning-based Knowledge Discovery techniques into the IEC 61499 standard shows potential for effectively extracting variability from control software.

Publication: 2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2024

ISSN: 1946-0740

ISBN: 979-8-3503-6124-7

DOI: 10.1109/ETFA61755.2024.10710711

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10710711

Publisher: IEEE

## Deodorant for Shotgun Surgery Bad Smell in IEC 61499-Based Control Software

Authors: Dunja Životin; Lisa Sonnleithner; Alois Zoitl

Author Affiliations: CDL VaSiCS; CDL VaSiCS; CDL VaSiCS

Keywords: IEC 61499; Bad Smells; Shotgun Surgery; Visualization; Computer languages; Source coding; Programmable logic devices; Surgery; Software; Maintenance; IEC Standards; Manufacturing automation; Software engineering

Abstract: Bad smells negatively influence different aspects of software, such as maintainability and quality. From development to maintenance, smells contribute to error-proneness and control software is no exception. Code smells are starting to gain some popularity in the domain of industrial automation and programming languages for Programmable Logic Controllers. However, they are still not as well researched as in general Software Engineering and lack appropriate support. Shotgun Surgery is a type of bad smell which can occur when changing source code. If every time a functionality is updated, many of the places where it is used need to be updated as well - we can sniff out Shotgun Surgery. This poses different challenges: being aware of all the places where this particular functionality is used and correctly updating those places. We aim to bridge the gap between bad smells and control software partially. We want to do this by developing approaches for automatic detection, visualization, and refactoring of Shotgun Surgery in IEC 61499 applications in Eclipse 4diac IDE.

Publication: 2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2024

ISSN: 1946-0740

ISBN: 979-8-3503-6124-7

DOI: 10.1109/ETFA61755.2024.10710951

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10710951

Publisher: IEEE

## Variability Extraction Methodologies for Developing Reusable Control Software Artifacts in IEC 61499

Authors: Shubham Sharma; Dunja Životin; Hafiyyan Sayyid Fadhlillah; Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; CDL VaSiCS; CDL VaSiCS; CDL VaSiCS

Keywords: Variability Extraction; Systematic Reuse; SPL; Maintenance; CPPS; Control Software; IEC 61499; Production systems; Systematics; Statistical analysis; Software; Maintenance; Proposals; History; IEC Standards; Manufacturing automation

Abstract: Control software in the Cyber-Physical Production System domain continuously evolves to cater to customer needs. Addressing customer needs involves developing new functional requirements or modifying existing functionalities, leading to the creation of product variants. Clone-and-own is a common reuse strategy in which the closest variant in project history is cloned and then modified to derive a new variant. Platform-oriented reuse is an alternative strategy that builds a configurable platform to derive variants. Adopting both reuse strategies for existing systems requires common and variant-specific artifacts to be extracted and maintained. This paper proposes two extraction methodologies that extract common and variant-specific artifacts from existing systems for systematic reuse. We evaluate the two extraction methodologies by applying them to multiple industrial and academic control software case study systems developed using IEC 61499. We conduct quantitative analysis of the extracted artifacts, considering factors such as the total effort required to derive variants, the number and size of artifacts that need maintenance, and their evolution using the two extraction methodologies. Our proposal suggests different variants of control software that lead to the creation of artifacts that are not only more optimal but also easier to maintain using a specific extraction methodology.

Publication: 2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2024

ISSN: 1946-0740

ISBN: 979-8-3503-6124-7

DOI: 10.1109/ETFA61755.2024.10711077

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10711077

Publisher: IEEE

## Visualization Tools for Machine Learning Pipelines: A Review

Authors: Valentina Golendukhina; Michael Felderer; Lisa Sonnleithner

Author Affiliations: University of Innsbruck, Innsbruck, Austria; German Aerospace Center (DLR), Institute for Software Technology University of Cologne, Cologne, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Human-centered computing—Visualization—Visualization systems and tools; Computing methodologies—Machine Learning; Visualization; Directed acyclic graph; Reviews; Pipelines; Data visualization; Machine learning; Visual systems; Complexity theory; Usability; Monitoring

Abstract: The increasing complexity and adoption of machine learning (ML) pipelines has led to a rising demand for effective visualization tools. This paper presents a comprehensive review of existing tools for visualizing data flow in machine learning (ML) pipelines. We highlight the tools’ purposes, integration methods, and visualization techniques. We collected and analyzed 22 open-source tools and concepts, analyzing their features and classifying them based on their primary purpose. Our analysis revealed five main purposes of visualization tools: exploration, explanation, visual development, comparison, monitoring. We provide an analysis of their integration methods, from standalone visual interfaces to code-level libraries, as well as a review of various visualization techniques, including Directed Acyclic Graphs (DAGs), pipeline matrices, and annotated visualizations. Our findings highlight the importance of visualization in enhancing the interpretability and efficiency of ML workflows. Moreover, the paper provides key limitations and challenges in current visualization methods to promote future research directions enhancing the usability and functionality of ML pipeline visualization tools.

Publication: 2025 IEEE 18th Pacific Visualization Conference (PacificVis)

Year: 2025

ISSN: 2165-8765

ISBN: 979-8-3315-0582-0

DOI: 10.1109/PacificVis64226.2025.00049

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11021023

Publisher: IEEE

## Component-based Control Software design using IEC 61499 Adapter Interfaces

Authors: Shubham Sharma; Alexander Stummer; Lisa Sonnleithner; Alois Zoitl

Author Affiliations: CDL VaSiCS; LIT CPS Lab, Johannes Kepler University Linz, Austria; CDL VaSiCS; CDL VaSiCS

Keywords: Design Patterns; Maintenance; Reusability; CPPS; Generic Components; IEC 61499; Adapter Interfaces; Visualization; Software design; Software; Sensor systems; Complexity theory; Sensors; Maintenance; Logic; IEC Standards; Manufacturing automation

Abstract: Control software components in the Cyber-Physical Systems domain use Function Blocks (FBs) to implement system logic, which manages interactions among hardware components (e.g., sensors and actuators) and other control software modules. FBs provide discrete input and output interfaces that support unidirectional data and event connections, which facilitate the integration of multiple subsystems to meet overall system requirements. However, this design based on discrete interfaces results in a high number of connection instances and lacks encapsulation. The complexity is further compounded by implicit one-to-many (fan-out) connections among subsystems, which can hinder both system understandability and maintainability. To address these challenges, we propose leveraging the adapter interface concept from IEC 61499. This approach replaces multiple discrete connections with a single bidirectional adapter connection that explicitly defines interaction requirements between components. Consequently, this reduces visual complexity and enhances system maintainability and testability.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205630

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205630

Publisher: IEEE

## A Formal Model Transformation from Data Flow Models to IEC 61499 Models

Authors: Malte Grave; Markus Meingast; Verena Klös; Alois Zoitl; Lisa Sonnleithner; Jörg Walter

Author Affiliations: CDL VaSiCS, Johannes Kepler University, Linz, Austria; LIT CPS Lab, Johannes Kepler University, Linz, Austria; Embedded Hardware-/Software-Systems, Carl von Ossietzky University of Oldenburg, Oldenburg, Germany; CDL VaSiCS, Johannes Kepler University, Linz, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria; OFFIS e.V., Oldenburg, Germany

Keywords: IEC 61499; data flow; model transformation; signal processing; GNU Radio; Eclipse 4diac; Runtime; Semantics; Signal processing algorithms; Transforms; Signal processing; Filtering algorithms; Syntactics; Data models; IEC Standards; Standards

Abstract: Signal processing plays a vital role in various areas of engineering, particularly in industrial automation. Signal processing applications are based on a data flow paradigm, which uses directed graphs to describe the flow of data between operations. Although industrial control applications are based on standards such as IEC 61499, their syntax, and semantics differ from the data flow paradigm, creating a challenge in integrating signal processing applications into industrial automation systems. Modeling signal processing applications using IEC 61499 is not yet a common practice. This paper addresses this gap by proposing an approach to transform data flow models into IEC 61499 models. This approach enables the design and transformation of signal processing applications using data flow models, without requiring manual modeling or knowledge of the IEC 61499 standard. The model transformation is formally defined and subsequently implemented as a separate tool. A running example illustrates the transformation process, demonstrating that the model is both syntactically correct and executable.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205747

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205747

Publisher: IEEE

## Maintainable Control Software Design Using Design Patterns in IEC 61499

Authors: Shubham Sharma; Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Control software design; design patterns; IEC 61499; restructuring; variability maintenance; Design methodology; IEC; Software; Measurement; Algorithms; Abstracts; Sockets; Filtering; Filters; Plugs

Abstract: Control software design in cyber-physical systems plays a vital role in ensuring maintainability and adaptability in response to evolving process requirements. Variability-aware designs facilitate the efficient integration of new functionalities and depend on the selected design elements and on the way these elements interact. Designers can enhance flexibility by applying design patterns and adopting alternative design elements when an existing design requires substantial modification effort. In IEC 61499, using discrete interfaces as a design element in function block (FB) implementations often incurs high effort due to numerous discrete connection instances and limited encapsulation. Complexity is further increased by implicit one-to-many connections among subsystems, which negatively affect system understandability and maintainability. This article analyzes two baseline implementations that follow pure service-oriented architecture (SOA) interaction patterns: choreography and orchestration, implemented in IEC 61499 using FBs with discrete interfaces. We then restructure these baseline implementations using design patterns and adapter interfaces, resulting in two new implementations with adapter interfaces and a hybrid interaction structure. We evaluate modification effort across three variability cases to quantify the changes required in the original and redesigned implementations. The results demonstrate a measurable reduction in modification effort and improvements in control software maintainability. Based on these findings, we derive guidelines to support practitioners in selecting suitable designs and interface strategies for a specific variability context in control software design.

Publication: IEEE Open Journal of the Industrial Electronics Society

Year: 2026

ISSN: 2644-1284

ISBN:

DOI: 10.1109/OJIES.2026.3705534

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11570863

Publisher: IEEE

## A Software Measure for IEC 61499 Basic Function Blocks

Authors: Lisa Sonnleithner; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; distributed control system; software measure; software metric; Software metrics; Design methodology; Software quality; Programming; Solids; Control systems; Software measurement

Abstract: When proposing new design patterns or design guidelines for IEC 61499 Applications, their performance and quality has to be compared to alternative solutions. Software measures are a way of achieving that. Although first attempts towards software measures for IEC 61499 were made, the standard still lacks a solid set of measures to evaluate applications. Taking a first step in that direction, we propose a set of measures for an IEC 61499 Basic Function Block.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212090

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212090

Publisher: IEEE

## Structuring Distributed Control Applications for Adaptability

Authors: Bianca Wiesmayr; Lisa Sonnleithner; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; distributed control system; reuse; adaptability; design rules; IEC Standards; Valves; Complexity theory; Software; Computer architecture; Hardware; Task analysis

Abstract: In modern industrial applications, the complexity of control software is increasing while its execution may be distributed to numerous small devices. The standard IEC 61499 fosters designing distributed control applications by defining a platform-independent application model that can be mapped to numerous hardware components. Applications though need to be designed for distribution, as comparing three implementation designs of a running example indicated. We propose the usage of a distributed architectural pattern for applications with parallel paths. Metrics confirm a reduced complexity compared to purely hierarchical designs.

Publication: 2020 IEEE Conference on Industrial Cyberphysical Systems (ICPS)

Year: 2020

ISSN:

ISBN: 978-1-7281-6390-1

DOI: 10.1109/ICPS48405.2020.9274744

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9274744

Publisher: IEEE

## Do you smell it too? Towards Bad Smells in IEC 61499 Applications

Authors: Lisa Sonnleithner; Michael Oberlehner; Elene Kutsia; Alois Zoitl; Sándor Bácsi

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; Budapest University of Technology and Economics, Budapest, Hungary

Keywords: IEC 61499; distributed control system; CPS; CPPS; design smell; code smell; bad smell; anti-pattern; OCL; Codes; Conferences; Maintenance engineering; Control systems; Software; IEC Standards; Manufacturing automation

Abstract: Bad Smells are certain suboptimal structures or patterns in software. They can cause maintenance issues and hinder understandability. Therefore, it is essential to avoid Bad Smells in software. While the topic is well researched in other fields, it is still an open issue in industrial automation. In this work, we are taking a step towards closing that gap and propose a catalog of IEC 61499 Bad Smells.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613379

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613379

Publisher: IEEE

## Catalog of Refactoring Operations for IEC 61499

Authors: Michael Oberlehner; Lisa Sonnleithner; Bianca Wiesmayr; Alois Zoitl; CDL VaSiCS

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Cyber-Physical Production System; Refactoring; Model-Driven Software Engineering; Production systems; Conferences; Software systems; Complexity theory; IEC Standards; Manufacturing automation; Software engineering

Abstract: Refactoring is a key technology for improving the quality of a software system. A higher quality will lead to a clearer structure, which facilitates sharing work across multiple teams. This is important especially in the domain of cyber-physical production systems, where different engineering disciplines meet at their cutting point. IEC 61499 tries to abstract the increasing complexity of such systems. This work gives an overview of existing refactoring techniques from software engineering and provides a first insight on how to apply refactoring to IEC 61499 systems.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613398

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613398

Publisher: IEEE

## IEC 61499 Distributed Design Patterns

Authors: Lisa Sonnleithner; Bianca Wiesmayr; Virendra Ashiwal; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Distributed control system; Software design; Software architecture; Distributed design; Design pattern; skill; choreography; Conferences; Decentralized control; Tools; Libraries; IEC Standards; Manufacturing automation

Abstract: IEC 61499 emerged as a language for modeling distributed control systems. An Application is a platform-independent model that is comprised of modular components. High reusability of these components and high reconfigurability of the underlying system configuration can only be achieved with advanced design patterns. We show two example implementations of such designs and extended a pattern to foster reuse. All designs are compared based on a set of evaluation criteria. We show that our proposed design provides improved understandability and adaptability, while maintaining a slim library with highly reusable Function Block types.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613569

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613569

Publisher: IEEE

## Automation Software Architecture in CPPS - Definition, Challenges and Research Potentials

Authors: Birgit Vogel–Heuser; Eva–Maria Neumann; Juliane Fischer; Marga Marcos; Elisabet Estévez Estévez; Giacomo Barbieri; Lisa Sonnleithner; Rick Rabiser

Author Affiliations: Institute of Automation and Information Systems TUM School of Engineering and Design Core Member of MDSI, Member of MIRMI Technical University of Munich, Garching, Germany; Institute of Automation and Information Systems TUM School of Engineering and Design Technical University of Munich, Garching, Germany; Institute of Automation and Information Systems TUM School of Engineering and Design Technical University of Munich, Garching, Germany; Department of Automatic Control and System Engineering, ETSI Bilbao Basque Country University, Bilbao, Spain; Electronics and Automation Engineering Department, University of Jaén, Jaén, Spain; Department of Mechanical Engineering, Universidad de los Andes, Bogotá, Colombia; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Cyber-Physical Production Systems; Automation Software Architecture; Programmable Logic Controllers; Computer science; Production systems; Software architecture; Conferences; Computer architecture; Cyber-physical systems; Software

Abstract: The importance of a mature, maintainable design of automation software in Cyber-Physical Production Systems (CPPS) is continuously increasing since a growing proportion of the system functionality is implemented via software. As a result, system complexity is shifting more and more towards the software side. Quality characteristics such as flexibility, maintainability, and extensibility, whose importance is increasing in the context of Industry 4.0, are thus becoming harder to achieve. These challenges can only be solved through sound architectural design. While there is a common understanding of good software architecture and appropriate methods to achieve it in computer science, a suitable architecture definition for automation software that takes all relevant factors into account is still missing in the field of CPPS. Therefore, based on a workshop with international scientists with different perspectives on CPPS, this paper presents influencing factors on automation software architecture. On this basis, a joint definition for software architecture in CPPS, as well as challenges and future research potentials, are derived.

Publication: 2022 IEEE 5th International Conference on Industrial Cyber-Physical Systems (ICPS)

Year: 2022

ISSN:

ISBN: 978-1-6654-9771-8

DOI: 10.1109/ICPS51978.2022.9816893

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9816893

Publisher: IEEE

## Identifying repeating patterns in IEC 61499 systems using Feature-Based embeddings

Authors: Markus Unterdechler; Antonio M. Gutiérrez; Lisa Sonnleithner; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: cyber-physical systems; artificial intelligence; IEC 61499; Industries; Production systems; Maintenance engineering; Software; Hardware; IEC Standards; Task analysis

Abstract: Cyber-Physical Production Systems (CPPSs) are highly variable systems of systems comprised of software and hardware interacting with each other and the environment. The increasing integration of technologies and devices has brought an unprecedented level of automation and customization. At the same time, it has also increased the efforts to maintain highly complex and heterogeneous systems. Although engineering practices support the reuse of common components to ease the development and maintenance of the systems in different projects, the identification of common components is still manually performed, which is a time-consuming, error-prone task. In this paper, a novel approach identifying repeating patterns in CPPSs based on artificial intelligence techniques is presented. This approach allows finding exact and similar components to support the CPPS design. Furthermore, it enables the maintenance of common components by reusing predefined types thereby reducing development effort. We implemented and evaluated our approach in an industry case study on developing CPPS control software with IEC 61499.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921527

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921527

Publisher: IEEE

## Architectural Concepts for IEC 61499-based Machine Controls: Beyond Normal Operation Handling

Authors: Lisa Sonnleithner; Bianca Wiesmayr; Virendra Ashiwal; Shubham Sharma; Alois Zoitl; Jörg Walter

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; CDL VaSiCS; OFFIS – Institute for Information Technology, Oldenburg, Germany

Keywords: IEC 61499; Distributed control system; Software design; Software architecture; Distributed design; Design pattern; Skill; Choreography; Error detection; Error handling; Production systems; Software design; Machine control; Design methodology; Decentralized control; Reliability engineering; Software

Abstract: Modern production systems are constantly getting more complex and moving towards smaller lot sizes and more customizable products. This poses new challenges on the control software, which is growing in size and complexity. To deal with this increasingly large and complex control software, design guidelines are needed. We are working on such design guidelines for IEC 61499, a modeling language for distributed control systems. In our previous work, we proposed a distributed and highly reusable application design based on skills. In this work, we will present concepts for extending this design beyond normal operation handling.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921610

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921610

Publisher: IEEE

## Applying Visualization Concepts to Large-Scale Software Systems in Industrial Automation

Authors: Lisa Sonnleithner; Philipp Bauer; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; CPS; CPPS; software visualization; circle packing; hierarchical edge bundling; Measurement; Manifolds; Visualization; Production systems; Automation; Codes; Conferences

Abstract: In recent years, the field of industrial automation is experiencing a dramatic increase of software development and maintenance effort. Driven by shorter product life-cycles and customizable products, production systems are becoming more and more complex, presenting new challenges for control software engineers. In this paper, we report on a visualization concept we applied to industrial automation software. It allows automation software developers to take a look at their software system from a new perspective. Various ways of interacting with the visualization offer further benefits, such as the convenient tracing of control and information flow across multiple hierarchies. We conducted a workshop with five industrial domain experts as a first evaluation of the usefulness of the visualization. Based on their feedback, we discuss open questions and next steps.

Publication: 2022 Working Conference on Software Visualization (VISSOFT)

Year: 2022

ISSN: 2379-7576

ISBN: 978-1-6654-8093-2

DOI: 10.1109/VISSOFT55257.2022.00029

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9978535

Publisher: IEEE
