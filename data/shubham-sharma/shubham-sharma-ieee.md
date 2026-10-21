## Modular Control Software Design to Support Mechatronic Variants in IEC 61499

Authors: Shubham Sharma; Hafiyyan Sayyid Fadhlillah; Antonio M. Gutiérrez Fernández; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Cyber-Physical Production System; IEC 61499; Modularization; Software Product Line; Control-Software; Actuators; Mechatronics; Software design; Maintenance engineering; Software; Sensor systems; Software reliability

Abstract: Cyber-Physical Production Systems (CPPSs) consist of deeply intertwined physical and software components. In the last decade, the number of mechatronic components (sensors, actuators, etc.) in a system is increasing enormously to enable more flexible, intelligent production with more support for customization. Mechatronic variability, like different variants of sensors or actuators in the system, directly affects the control software. The standardization of physical interfaces of mechatronic components has provided well-defined plug-and-play interaction. Conversely, software components in the CPPS domain still face the issue of standardizing functionality. Software adaptability often leads engineers to develop control software for new mechatronic variants by just copying and modifying existing software. This leads to multiple and completely separate instances of the control software and a high development and maintenance effort. The core functionality of the control software should be standardized and reused as much as possible to reduce the development effort and improve overall reliability. This paper discusses an approach to standardize core functionality of IEC 61499-based control software. Our design approach encapsulates the process core functionality and defines standard interfaces for interacting with mechatronic variant software components. We evaluate our design approach by comparing it to the traditional clone-and-own approach for an academic case study system, a capping station. Additionally, we assess the impact of adding a new variant in the control software and analyze what changes are needed to keep the same core functionality. When introducing new mechatronic variants in combination with standardized core functionality, our design approach reduces the overall control software variance and maintenance effort.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275333

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275333

Publisher: IEEE

## Delta Models as a Measurement for Improving the Quality of IEC 61499-based Control Software

Authors: Prankur Agarwal; Shubham Sharma; Hafiyyan Sayyid Fadhlillah; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Delta Modeling; Software Measurements; Software Adaptability; Couplings; Adaptation models; Software architecture; Computer architecture; Size measurement; Software; Hardware

Abstract: Industrial-scale control software is designed as variability-intensive, i.e., highly configurable and adaptable software, to support diverse hardware capabilities and to fulfill diverse customer requirements. Various control software architectures have been proposed for developing highly configurable and adaptable control software. However, each architecture has its strengths and weaknesses in configurability and adaptability. Measuring the suitability of a given architecture to deal with variability can further guide control software engineers in implementing highly configurable and adaptable control software. In this paper, we propose measurement approaches for IEC 61499-based control software that indicate how well a particular architecture can manage variability. Control software engineers are first encouraged to describe all the functionalities in their system. They can also describe which elements must be added or removed when implementing a particular functionality. They then store these descriptions using a variability mechanism called delta models. Next, we can measure the size of delta models, the cohesion and coupling of the control software modules, and the degree of mapping complexity between features and delta models. We argue that by using our proposed measurements, we can indicate whether the control software’s architecture is suitable for variability-intensive software.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275452

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275452

Publisher: IEEE

## Delta Modeling in IEC 61499: Expressing Control Software Variability in Cyber-Physical Production Systems

Authors: Hafiyyan Sayyid Fadhlillah; Shubham Sharma; Antonio M. Gutierrez Fernandez; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Software Variability; Delta Modeling; Production systems; Systematics; Maintenance engineering; Software; Software product lines; IEC Standards; Usability

Abstract: IEC 61499 is a standard for developing distributed industrial control software. It supports the configurability of the control software as the application model is platform-independent and separated from the system model that defines the hardware configuration specification. Thus, it can be used to develop control software for highly configurable Cyber-Physical Production Systems (CPPS). To address their customers’ requirements, companies that build CPPSs over time develop many variants of such production systems, typically through clone-and-own reuse, which increases engineering and maintenance efforts. Managing the control software variability in CPPSs in a systematic manner would facilitate software reuse and reduce the cost of developing and maintaining these systems. However, the IEC 61499 standard itself offers only limited capabilities for managing variability, e.g., by utilizing a library of modular components or by following certain design patterns. In this paper, we propose an approach to systematically manage IEC 61499-based control software using a (textual) delta modeling approach. Delta modeling is a prominent concept in the Software Product Line (SPL) domain for expressing and maintaining software variability. We show how our delta modeling approach can express control software variability and provide a semi-automatic control software generator. We evaluate the usability of our approach by applying it to multiple case studies as well as by performing a user study, in which control software engineers used our delta modeling approach. Our evaluation results indicate potential benefits of our delta modeling approach to implement and maintain control software through software generation.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275693

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275693

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

## Dashboard Tool for Supporting Control Software Variability Maintenance in Industrial Automation

Authors: Shubham Sharma; Alexander Stummer; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; CDL VaSiCS

Keywords: Control Software Maintenance; Variability Extraction Data; Software Product Line; Feature Mapping; CPPS; Software maintenance; Production systems; Systematics; Prototypes; Cyber-physical systems; Feature extraction; Software product lines; Maintenance; Data mining; Software development management

Abstract: Control software in the Cyber-Physical Production System domain continuously evolves to meet customer needs, resulting in multiple software variants that require effective management. Developers often adopt ad hoc techniques such as Clone-and-Own to generate new product variants. These offer short-term benefits but pose long-term maintenance challenges. Such cloned product variants contain numerous artifacts with diverse associations, exhibiting commonalities as well as variability across different variants and versions. Various approaches exist to identify these commonalities and variability and extract reusable artifacts from product variants to support systematic reuse. However, existing approaches are typically limited to particular programming languages and have not been applied to control software. Also, there is a lack of tool support to analyze, visualize, and store variable artifacts across multiple product variants. This paper introduces a prototype dashboard tool to enhance the analysis, visualization, and representation of control software artifacts across multiple product variants. The tool provides the foundation for adopting a Software Product Line engineering approach for control software development.

Publication: 2025 IEEE 8th International Conference on Industrial Cyber-Physical Systems (ICPS)

Year: 2025

ISSN: 2769-3902

ISBN: 979-8-3315-4300-6

DOI: 10.1109/ICPS65515.2025.11087906

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11087906

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

## Rule-based Redesign of Abstract GraphML Representations into IEC 61499-Oriented Designs

Authors: Shubham Sharma; Oleksandr Kudriavchenko; Felix Schmid; Alois Zoitl

Author Affiliations: CDL VaSiCS; CDL VaSiCS; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS

Keywords: GraphML; IEC 61499; Rule-based redesign; Interface strategies; Pre-design analysis; CPPS; IEC; Modeling; Design methodology; Software; Abstracts; Printing; Indium phosphide; Joining processes; Technology

Abstract: This paper presents an approach for deriving IEC 61499-oriented designs from abstract GraphML representations. GraphML is a graph-based language that can represent systems, their components and interactions as a graph. Such representations are useful for communicating top-level system designs and onboarding new team members. However, they mainly capture structural information and lack the IEC 61499-specific design decisions required for control software development. These decisions include the number and type of interfaces, hierarchy levels, and interface connections across nested structures. In systems with many components and deep hierarchies, manually selecting an interface strategy and analyzing its effect on the overall system structure is cumbersome and error-prone. To address this issue, we propose a rule-based redesign approach that redesigns abstract GraphML representations into IEC 61499-oriented GraphML representations. The resulting design preview supports the review and analysis of key IEC 61499 design decisions before implementation. The approach is grounded in practical field experience and discussions with control software engineers, and it supports maintainable and cost-effective control software development.

Publication: 2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2026

ISSN: 1946-0740

ISBN: 979-8-3315-7889-3

DOI: 10.1109/ETFA68377.2026.11724872

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11724872

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

## Supporting Variability Management in Cyber-Physical Production Systems: Towards Semi-Automatic Delta Model Mining for IEC 61499

Authors: Hafiyyan Sayyid Fadhlillah; Shubham Sharma; Rick Rabiser; Alois Zoitl

Author Affiliations: CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Variability Mining; Delta Modeling; Cyber-Physical Production System; Software Product Line; Production systems; Systematics; Maintenance engineering; Software; Sensor systems; Sensors; Recording

Abstract: Cyber-Physical Production Systems (CPPSs) are complex, highly-configurable systems interacting with their environment by sensors and actuators. Software in CPPS typically exists in a plethora of variants, developed to fulfill customer and technology requirements, which have to be maintained over a long time. Support for variability management can foster systematic reuse and configurability, but this requires a significant investment of resources to explicitly document or model variability. Additionally, we need to define the reusable engineering artifacts and their variability corresponding to the documents or models. Furthermore, the documents or models need to be maintained and kept consistent with the artifacts evolving frequently. In this short paper, we propose to (semi-)automatically capture delta models describing differences be-tween CPPS control software variants and support generating these variants based on a product line platform. Specifically, we envision a change recording mechanism and model comparison approaches for control software developed using IEC 61499, a domain-specific modeling language used for developing distributed control in CPPSs. We argue that both approaches can significantly reduce the development and maintenance effort for delta models.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921660

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921660

Publisher: IEEE
