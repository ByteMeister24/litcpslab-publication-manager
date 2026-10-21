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

## A Proposal for OPC UA Companion Specification for IEC 61499 Based Control Application

Authors: Mainak Majumder; Alois Zoitl

Author Affiliations: CDL VaSiCS; CDL VaSiCS

Keywords: Communication; Function Blocks; IEC 61499; Information Model; OPC UA; Automation; Software architecture; Computer architecture; Software systems; Proposals; Internet of Things; IEC Standards

Abstract: The introduction of emerging technologies like the Internet of Things (IoT), Artificial Intelligence (AI), and Cloud computing have radically evolved the software architecture of the industrial automation domain. Future automation and control software systems require a flexible and open architecture. The IEC 61499 standard-based programming paradigm, due to its flexible and modular structure, is considered a potential tool for developing future automation systems. Therefore, integrating IEC 61499 standard with the Open Platform Communication Unified Architecture (OPC UA) could be beneficial as it will increase the applicability of the standard. However, no formal mapping between the IEC 61499 models and the OPC UA information model is defined by the OPC Foundation for now. Therefore, in this paper, a conceptual mapping between the models of these two standards is provided. The goal of this work is to develop an OPC UA companion specification for the IEC 61499.

Publication: 2023 IEEE 19th International Conference on Factory Communication Systems (WFCS)

Year: 2023

ISSN: 2835-8511

ISBN: 978-1-6654-6433-8

DOI: 10.1109/WFCS57264.2023.10144247

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10144247

Publisher: IEEE

## Close Enough? Criteria for Sufficient Simulations of IEC 61499 Models

Authors: Bianca Wiesmayr; Sven Mehlhop; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Austria; Carl von Ossietzky University of Oldenburg, Germany; LIT CPS Lab, Johannes Kepler University Linz, Austria

Keywords:

Abstract: The IEC 61499 standard defines a model for distributed control systems based on function blocks (FBs) and event-driven execution. Although interoperability and portability between tools are core goals of the standard, the behavior of an executable model varies significantly between run-time environments (RTEs). This presents challenges for comparing execution traces, e.g., when validating that a simulation of an IEC 61499 model conforms to a specific RTE. In this paper, we propose a methodology for analyzing the behavior of custom IEC 61499 RTEs based on example models that cover specific language features or known semantic variants. These examples are derived from an analysis of the standard and relevant literature on IEC 61499 semantics. We founded a publicly available repository of collected examples that can be used to analyze the RTE behavior in a structured way. Our approach provides a starting point for a future comprehensive set of example models. In this paper, we focus on FB network execution and demonstrate the effectiveness of our approach by comparing the behavior of 4diac FORTE and a model simulator. Our methodology offers a systematic and practical way for identifying implemented semantic variants of IEC 61499.

Publication: 2023 IEEE 19th International Conference on Automation Science and Engineering (CASE)

Year: 2023

ISSN: 2161-8070

ISBN: 979-8-3503-2070-1

DOI: 10.1109/CASE56687.2023.10260555

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10260555

Publisher: IEEE

## Supporting Model-Based Network Specification for Time-Critical Distributed Control Systems in IEC 61499

Authors: Friederike Bruns; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: OFFIS e.V. Oldenburg, Germany; LIT CPS Lab, Johannes Kepler University, Linz, Austria; LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords:

Abstract: Designing the software for distributed control systems introduces new challenges regarding handling the communication between devices. The domain-specific modeling language defined in IEC 61499 provides mechanisms to distribute software across devices, but does not provide modeling elements for describing details about the communication between these devices. We provide an extensible proof-of-concept implementation for specifying the communication of an IEC 61499-based system that extends the current system model. Our approach requires only minimal adaptations of the IEC 61499 standard and proposes an extensible concept for modeling various kinds of communication protocols. We integrated the concept into an open-source development environment for IEC 61499. We then evaluated the approach and the tool by configuring time-sensitive networking for a typical control application. Engineers can customize our approach with low effort to support additional paradigms for communication using the provided extension mechanisms.

Publication: 2023 IEEE 19th International Conference on Automation Science and Engineering (CASE)

Year: 2023

ISSN: 2161-8070

ISBN: 979-8-3503-2070-1

DOI: 10.1109/CASE56687.2023.10260604

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10260604

Publisher: IEEE

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

## Towards Integrating Interface Behavior Models for Components of Distributed Control Software

Authors: Bianca Wiesmayr; Antonio M. Gutierrez Fernandez; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; CDL VaSiCS

Keywords: IEC 61499; Control Software; Interface Behav-ior Models; Adaptation models; Decentralized control; Production; Software; Hardware; Behavioral sciences; IEC Standards

Abstract: Modeling distributed control software facilitates reacting to changing hardware configurations due to the higher abstraction level. Well-designed modules of such systems may be arranged flexibly to perform production tasks, which need to be adapted during the life-cycle of the system. Although IEC 61499 supports modeling the relations between inputs and outputs of its software components as service sequence models, these models are not integrated with the rest of the development process. In this paper, we outline our vision of using the captured information on the interface behavior for development tasks of distributed control software modeled according to IEC 61499. The proposed research directions can contribute to the acceptance of modeling methods in the domain, as appropriate tool support can notably leverage the benefit of models.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275397

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275397

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

## A Domain-Driven Design Oriented OPC UA Server Development Methodology for CPPS

Authors: Mainak Majumder; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: CPPS; Domain-driven design; Information Model; Layered Architecture; OPC UA; Production systems; Software architecture; Architecture; Buildings; Computer architecture; Aging; Software

Abstract: Software has become an integral part of production automation systems and it is going to play a key role in the realization of Cyber-Physical Production Systems (CPPSs), a software-defined futuristic smart production environment. However, the emergence of CPPS has led to the development of a new genre of software tools that aims to bridge the gap between the machine world and the software domain. Examples of such tools are Open Platform Communication Unified Architecture (OPC UA) based software applications that are seen as potential enablers for CPPS. Building OPC UA server applications for CPPS could pose multiple challenges which could be addressed using established software development approaches. In this paper, we investigated the well-known Domain-Driven Design (DDD) based software development concept and its applicability regarding the development of an OPC UA server application for CPPS.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275496

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275496

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

## Maturity Evaluation of Domain-Specific Language Ecosystems for Cyber-Physical Production Systems

Authors: Sandra Greiner; Bianca Wiesmayr; Kevin Feichtinger; Kristof Meixner; Marco Konersmann; Jérôme Pfeiffer; Michael Oberlehner; David Schmalzing; Andreas Wortmann; Bernhard Rumpe; Rick Rabiser; Alois Zoitl

Author Affiliations: Software Engineering Group, University of Bern, Switzerland; LIT CPS Lab, Johannes Kepler University Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Austria; CDL SQI, Institute of Information Systems Engineering, Technische Universität Wien, Austria; Software Engineering, RWTH Aachen University, Germany; Institute for Control Engineering of Machine Tools and Manufacturing Units (ISW), University of Stuttgart, Germany; LIT CPS Lab, Johannes Kepler University Linz, Austria; Software Engineering, RWTH Aachen University, Germany; Institute for Control Engineering of Machine Tools and Manufacturing Units (ISW), University of Stuttgart, Germany; Software Engineering, RWTH Aachen University, Germany; LIT CPS Lab, Johannes Kepler University Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Austria

Keywords: Cyber-Physical Production Systems; Domain-Specific Languages; Development Tools; Industries; Production systems; Ecosystems; Process control; Companies; Software; Libraries

Abstract: Engineering Cyber-Physical Production Systems (CPPSs) heavily relies on Domain-Specific Languages (DSLs), which are tailored to a specific class of problems inherent to CPPSs. DSLs enable non-programming experts to solve problems in their domain, such as modeling production processes, implementing control software, or managing the variability of production systems. A DSL ecosystem encompasses the entire infrastructure (e.g., libraries and tools) built around its language and contributes to the successful and easy adoption thereof by domain experts. We present a maturity evaluation model for DSL ecosystems serving two aims: to developers, it reveals missing but essential aspects of the ecosystem, and users (e.g., industrial companies) can evaluate the maturity of a DSL ecosystem. We propose criteria to evaluate the maturity of DSL ecosystems and apply them to existing, publicly available DSLs which have been adopted in CPPSs. The results demonstrate that all components of the model are covered and they allow for deriving hypotheses about DSL ecosystems used in CPPSs.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275624

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275624

Publisher: IEEE

## Generating Por table Test Cases for IEC 61499 FBs from Interface Behaviour Specifications

Authors: Bianca Wiesmayr; Midhun Xavier; Sandeep Patil; Alois Zoitl; Valeriy Vyatkin

Author Affiliations: LIT CPS Lab, Johannes Kepler University, Linz, Austria; Department of Computer Science, Computer and Space Engineering, Lulea Tekniska Universitet, Sweden; Department of Computer Science, Computer and Space Engineering, Lulea Tekniska Universitet, Sweden; LIT CPS Lab, Johannes Kepler University, Linz, Austria; Department of Computer Science, Computer and Space Engineering, Lulea Tekniska Universitet, Sweden

Keywords: Model-Based Testing; IEC 61499; Function Blocks; Service Sequences; Portability; Visualization; Semantics; Cyber-physical systems; Software; IEC Standards; Manufacturing automation; Testing

Abstract: IEC 61499 is an executable, event-based language for control software that allows visual and textual implementation of individual software components (Function Blocks, FBs). The standardized visual service sequence model specifies the expected input/output behaviour of a component, thus supporting model-based testing. We present our approach for testing an FB on various platforms, which helps manage the variations in execution semantics between different vendors. First, service sequences are generated manually or derived from an existing (partial) implementation. Then, these service sequences serve as unit tests for this implementation. Finally, we create a test application that is executable on any IEC 61499-compliant platform. Executing tests directly in the target platform helps validate the correct functionality of an FB before deploying the control software to a cyber-physical system.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275633

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275633

Publisher: IEEE

## Exploring Refactoring Operations for IEC 61499

Authors: Michael Oberlehner; Andreas Eigner; Manuel Wimmer; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University, Linz; LIT CPS Lab, Johannes Kepler University, Linz; CDL-MINT, WIN-SE, Johannes Kepler University, Linz; LIT CPS Lab, Johannes Kepler University, Linz

Keywords: IEC 61499; Cyber-Physical Production System; Refactoring; Model-Driven Software Engineering; Systematics; Production; Maintenance engineering; Software; IEC Standards; Manufacturing automation; Software engineering

Abstract: In the domain of CPPS, long-term maintenance of software is necessary. Refactoring, a technique used to improve maintainability is a viable solution. However, there is a scarcity of research on refactoring in the context of CPPS. In this work, we propose a systematic approach for analyzing and deriving refactoring operations for IEC 61499. In particular, we propose a generic meta-model for block-based languages, which is accompanied by a corresponding generic refactoring catalog. Based on the generic meta-model, an existing refactoring catalog for IEC 61499 is extended by comparing and evaluating meta-models and their associated refactoring operations derived from literature of different modeling languages. We demonstrate that our approach provides a systematic way of transferring refactoring operations across block-based modeling languages and allows to extend existing refactoring collections for IEC 61499.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275635

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275635

Publisher: IEEE

## Composing Services with SMT-Based Deployment Optimization and Service Merging Heuristic

Authors: Tarik Terzimehić; Eddie Groh; Alois Zoitl

Author Affiliations: Fortiss – Research Institute of the Free State of Bavaria, Munich, Germany; Technical University Munich, Munich, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords: Industry 4.0; IEC 61499; deployment synthesis; service composition; optimization; SMT; Couplings; Scalability; Merging; Metaheuristics; Production; Programming; Complexity theory

Abstract: The complexity of Industry 4.0 systems makes it challenging to manually synthesize and optimize architecture-level decisions, such as service deployment and composition. To address this challenge, we propose an approach that utilizes a satisfiability modulo theories (SMT) solver to (semi-)automate service deployment and composition synthesis. Thereby, we conceptualize, formalize and implement the complete workflow from input service workflows to valid and optimized service deployments and compositions. We demonstrate the practical application of our approach in an Industry 4.0 scenario, specifically the flexible production of new products. We evaluate the effectiveness of the proposed approach by investigating its benefits in terms of engineering effort, complexity of the resulting IEC 61499-based applications, and improvement of communication coupling quality attribute (QA).

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275652

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275652

Publisher: IEEE

## Extending the OPC UA Companion Specification for an IEC 61499-based Control System

Authors: Mainak Majumder; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Companion specification; IEC 61499; OPC UA; Adaptation models; Production systems; Decentralized control; Semantics; Stakeholders; IEC Standards; Standards

Abstract: The IEC 61499-based distributed control model is gradually gaining popularity among the stakeholders involved in the field of cyber-physical production systems. Integration of IEC 61499 with the Open Platform Communication Unified Architecture (OPC UA) will ease the effort required for horizontal as well as vertical integration of distributed control applications. In our previous work, we mapped the function block model and the application model of the IEC 61499 standard to OPC UA. This work-in-progress paper is intended to be an extension of our previous work that demonstrates the mapping of the resource, device, and the system model to OPC UA.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275677

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275677

Publisher: IEEE

## Landscape of Architectural Design Decisions in Industry 4.0

Authors: Tarik Terzimehić; Alois Zoitl

Author Affiliations: Fortiss – Research Institute of the Free State of Bavaria, Munich, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords: I4.0; architecture synthesis; optimization; Production planning; Production; Computer architecture; Software; Fourth Industrial Revolution; Resource management; Object recognition

Abstract: Design of manufacturing system involves various architectural design decisions (ADDs), including software and hardware component allocation, production service composition, plant layout determination, and production planning. These ADDs gain significance in Industry 4.0 (I4.0) scenarios due to the frequent need for architecture synthesis to achieve adaptable and flexible production processes. Additionally, synthesizing ADDs in conjunction with each other increases the decisions’ impact on system quality attributes (QAs). The increasing importance of architecture synthesis and optimization (ASO) in I4.0 necessitates an overview of ADDs within this context. This paper expands on the previous work by creating a landscape of I4.0-related ADDs based on insights from the BaSys 4.0 research project series. The landscape describes relevant ADDs and their relationships, and suggests multi-dimensional ASO workflows. Mapping the ADD landscape to BaSys 4.0 research enhances idea generation and the exploration of existing solutions in ASO.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275678

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275678

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

## Run-time Configuration of the IEC 61499-based PLC-Service Bus via OPC UA

Authors: Mainak Majumder; Virendra Ashiwal; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; ABB Corporate Research Center Germany, Ladenburg, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Message-oriented middleware; OPC UA; PLC-Service bus; Adaptation models; Software architecture; Programmable logic devices; Programming; Software; Software reliability; Servers

Abstract: Modern industrial automation applications require a flexible and modular software architecture that can be easily adapted to meet dynamic market requirements. The IEC 61499-based programming model, due to its distributed and modular nature, could be a potential tool in this regard. In our previous works, we proposed the concept of a PLC-Service bus, a service-oriented architecture-based control application development paradigm for the Programmable Logic Controller (PLC). We have also demonstrated its applicability using the IEC 61499 modelling language. In this paper, we propose an OPC UA-based configuration approach for software components of the PLC-Service bus.

Publication: 2023 IEEE 28th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2023

ISSN: 1946-0740

ISBN: 979-8-3503-3992-5

DOI: 10.1109/ETFA54631.2023.10275697

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10275697

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

## Enabling Automated Timing Verification: A Unified Approach for Industrial Distributed Control Systems

Authors: Friederike Bruns; Sven Mehlhop; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: Department of Computing Science, Carl von Ossietzky Universitä t Oldenburg, Oldenburg, Germany; Department of Computing Science, Carl von Ossietzky Universitä t Oldenburg, Oldenburg, Germany; LIT CPS Lab Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab Johannes Kepler University Linz, Linz, Austria

Keywords:

Abstract: In a correct control system, events are never late, nor are they early. They are delivered precisely when the engineer means to. IEC 61499 defines a modeling language for control software of distributed systems. However, timing requirements cannot be specified as part of an application model. As a result, deriving timing specifications for components is a separate and additional manual, i. e., non-automatized, step when designing a correct system. Contract-based design is a widely known approach for correct-by-construction system design. This work presents concepts and tool support for integrating timing specifications into IEC 61499 based on the MULTIC timing specification language. We applied our approach to a demonstration example to illustrate developing IEC 61499 systems following contract- based design. Any specified contracts are stored as part of sub- applications, which are a hierarchical structuring mechanism of IEC 61499. The resulting models can form the input for continuous timing verification of IEC 61499 models.

Publication: 2024 IEEE International Conference on Industrial Technology (ICIT)

Year: 2024

ISSN: 2641-0184

ISBN: 979-8-3503-4027-3

DOI: 10.1109/ICIT58233.2024.10540790

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10540790

Publisher: IEEE

## Multidimensional Design Space Exploration for Evolving Manufacturing Systems: Interplay of Deployment, Topology, and Production Planning Architectural Decisions

Authors: Tarik Terzimehić; Daniel Erler; Alois Zoitl

Author Affiliations: fortiss—Research Institute of the Free State of Bavaria, Munich, Germany; Technical University Munich, Munich, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Architecture synthesis; design space exploration (DSE); manufacturing; optimization; Production; Topology; Space exploration; Production planning; Software; Hardware; Fasteners; Manufacturing systems

Abstract: Optimizing evolving manufacturing systems often requires considering the interplay of various architectural design decisions (ADDs), especially at the lower levels of the automation pyramid. Here, decisions about programmable logic controllers, stations, and shop-floor topology directly impact product characteristics. This necessitates a multidimensional design space exploration (DSE) approach that synthesizes diverse ADDs together. However, integrating diverse ADDs within the complex context of industrial automation remains a challenge, and existing DSE solutions from other domains often lack direct applicability. This work introduces a novel multidimensional DSE approach for such systems, leveraging domain-specific input models to automatically generate valid and optimal deployment, shop-floor topology, and production planning ADDs. We evaluate the approach by assessing the quality of derived ADDs against various domain optimization goals. This evaluation compares our approach to both random and manual ADDs, utilizing a prototype implementation and realistic manufacturing architectures.

Publication: IEEE Transactions on Industrial Informatics

Year: 2024

ISSN: 1941-0050

ISBN:

DOI: 10.1109/TII.2024.3435373

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10638774

Publisher: IEEE

## Mitigating Conflicts in Architectural Design Decisions for Evolving Manufacturing Systems: Evaluation and Recommendations for Practitioners

Authors: Tarik Terzimehić; Alois Zoitl

Author Affiliations: fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords: Industry 4.0; DSE; optimization; SMT; ADD; Generative AI; Prevention and mitigation; Production planning; Production; Software; Topology; Space exploration; Planning; Optimization; Manufacturing systems

Abstract: The design process for manufacturing systems involves different architectural design decisions (ADDs), including deploying software to hardware components, determining shop-floor topology, and planning production tasks for stations. These ADDs exhibit complex interactions, where the synthesis of one ADD impacts other ADDs, highlighting the need to investigate their dynamic interplay. However, current research prioritizes individual ADDs over exploring multiple ADDs together. This work investigates a multi-dimensional design space exploration (DSE) of deployment, shop-floor topology, and production planning ADDs. We introduce mitigation constraints to ensure the compatibility among these ADDs. To evaluate our approach, we apply it to a flexible manufacturing line demonstrator. Furthermore, we assess and compare various DSE workflows, providing preliminary guidance to software architects on mitigatlng conflicts and enhancing the quality of ADDs.

Publication: 2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2024

ISSN: 1946-0740

ISBN: 979-8-3503-6124-7

DOI: 10.1109/ETFA61755.2024.10710879

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10710879

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

## Updating and Refactoring Library Modules in IEC 61499

Authors: Michael Oberlehner; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University, Linz, Austria; CDL VaSiCS

Keywords: Library Management; IEC 61499; Refactoring; Inconsistency Management; Software Evolution; Software maintenance; Visualization; Production systems; Automation; Prototypes; Focusing; Libraries; IEC Standards; Informatics; Standards

Abstract: This paper proposes a novel library management system tailored for Cyber- Physical Production Systems (CPPSs) using the IEC 61499 standard. Focusing on software maintenance challenges in CPPSs, we introduce efficient updating and refac-toring operations for modularized type libraries. Our approach addresses the unique requirements of graphical development environments, enhancing the longevity and efficiency of software maintenance. The workflow of creating, maintaining, and up-dating library modules is outlined, along with conflict detection, error visualization, and potential refactoring/update operations. Additionally, we illustrate the architectural concept implemented as a prototype in an IDE. The implemented library management system demonstrates its practical application through a case study. This research contributes to the ongoing development of robust software maintenance practices in industrial automation systems.

Publication: 2024 IEEE 22nd International Conference on Industrial Informatics (INDIN)

Year: 2024

ISSN: 1935-4576

ISBN: 979-8-3315-2748-8

DOI: 10.1109/INDIN58382.2024.10774367

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10774367

Publisher: IEEE

## Identification and Evaluation of Pitfalls in the Migration From IEC 61131-3 to IEC 61499: A Review

Authors: Virendra Ashiwal; Oscar Miguel-Escrig; Bianca Wiesmayr; Alois Zoitl; Julio-Ariel Romero-Pérez

Author Affiliations: ABB AG Corporate Research Center Germany, Mannheim, Germany; Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain

Keywords: Distributed control system (DCS); IEC 61131; IEC 61499; industrial automation; programmable logic controller (PLC) software; software modernization; IEC Standards; Standards; Codes; Automation; Systematic literature review; Industrial electronics; Unified modeling language; Computer languages; Decentralized control; Automation; Programmable logic devices

Abstract: The IEC 61131-3 standard was initially established to define a common software architecture and programming languages for programmable logic controllers (PLCs) produced by various manufacturers, leading to its widespread adoption since 1993. Since then, it has been a cornerstone in the industrial automation domain. Building upon this foundation, the IEC 61499 standard was developed to enhance the design and implementation of distributed control systems by incorporating advanced concepts from distributed systems and software engineering such as encapsulation, separation of control logic from communication infrastructure, and independent development of software components from their hardware deployment. While IEC 61499 introduces novel approaches, it also incorporates and extends key elements from IEC 61131-3, including function blocks, programming languages, and basic data types. Despite the advantages offered by the IEC 61499 standard, its adoption is still limited largely due to historical precedence, industry familiarity, better tool and vendor support, and the risk-averse nature of the industrial automation market. The migration or re-engineering effort from an existing IEC 61131-based automation system to IEC 61499 also faces challenges because it typically retains the underlying programming paradigms of IEC 61131-3. The contribution of this article is to identify the pitfalls associated with migrating PLC control code from IEC 61131-3-based automation systems to IEC 61499. For this purpose, we conducted a systematic literature review that address these identified migration pitfalls. We then synthesized the findings from the literature and provided a summary and research directions for addressing these pitfalls.

Publication: IEEE Open Journal of the Industrial Electronics Society

Year: 2025

ISSN: 2644-1284

ISBN:

DOI: 10.1109/OJIES.2025.3558685

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10955217

Publisher: IEEE

## A Systematic Literature Review of the Characteristics of Automation Systems That Impact Debugging of PLC Software

Authors: Jose Cabral; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Automation; PLC; debugging; software engineering; Debugging; Software; Automation; Systematic literature review; Libraries; Software development management; IEC Standards; Monitoring; Databases; Testing

Abstract: The debugging capabilities of software development tools in the automation domain lag behind other domains. Basic capabilities from regular debuggers, such as breakpoints and step-by-step execution, are hard to find or do not support all requirements imposed by the domain. This work presents the results of a Systematic Literature Review carried out to understand the characteristics of the automation domain that influence the debugging capabilities of Programmable Logic Controller (PLC) software and to find the current state and future directions of debugging tools. The process of the review was prepared and reviewed before its execution to avoid any type of bias. The review successfully finds the major characteristics affecting the debugging of PLC software which include the presence of interconnected components and heavy machinery from different domains, the participation of different stakeholders at different phases of the development of the automation systems, and the restricted software capabilities specific to the domain. The existing debugging capabilities are mainly limited to monitoring and forcing the current state of the PLC software. However, research is being done in different areas that help debug PLC software, such as testing and simulation, and static and dynamic code analysis. The latter helps develop more powerful debugging capabilities such as the reproduction of real-time scenarios and replay debugging. The usability of debugging tools is also a subject of study in the automation domain. The work ends with an overview of future research directions to close the gap to other domains. Note to Practitioners—This paper was motivated by the limited capabilities found when developing software for Programmable Logic Controllers (PLC) used in the automation domain. A Systematic Literature Review (SLR) was conducted to understand the reasons for the limited debugging capabilities and to know the current state of debugging tools in the automation domain. For the SLR, search terms were defined and used to look for research studies in different online libraries. The result of the search was filtered based on inclusion and exclusion criteria, and the remaining resources were read in detail. From the information found, the debugging capabilities in PLCs are limited due to the machinery connected to them, the different people involved while creating automation systems, and restrictions of programming standards used to develop software for PLCs. The current debugging capabilities for PLCs are mainly limited to monitoring the current state and forcing new ones. However, research has been done to extend the debugging capabilities in the areas of testing, simulation, static and dynamic code analysis, and reproduction of real-time scenarios. This paper provides at the end research directions to further improve debugging capabilities for PLC software.

Publication: IEEE Transactions on Automation Science and Engineering

Year: 2025

ISSN: 1558-3783

ISBN:

DOI: 10.1109/TASE.2025.3559790

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10965779

Publisher: IEEE

## Digital Twin Architecture Patterns for Real-Time Control Systems

Authors: Mainak Majumder; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: LIT CPS Lab Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS,LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: CPPS; Digital Twin; Models; Real-time Control; Manufacturing industries; Process control; Systems architecture; Production; System integration; Control systems; Real-time systems; Digital twins; Monitoring; Manufacturing systems

Abstract: Digital Twins (DTs) have become an emerging topic of research in the manufacturing and production domain. DTs are integrated into existing manufacturing systems to monitor, control, and optimize production processes. This in turn influences the requirements for system integration and logical system architecture. A better understanding of the relationship between the existing Real-Time (RT) process control systems and DTs can boost the adoption of DTs in the manufacturing industry. Therefore, in this paper, we investigate possible interaction patterns of DTs with RT process control systems and define four use case categories for using DTs, i.e., observing, operating, controlling, and engineering a manufacturing system.

Publication: 2025 IEEE 8th International Conference on Industrial Cyber-Physical Systems (ICPS)

Year: 2025

ISSN: 2769-3902

ISBN: 979-8-3315-4300-6

DOI: 10.1109/ICPS65515.2025.11087873

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11087873

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

## Trustworthy Human-Robot Collaboration programming using a Gantt chart-based Domain-Specific Modeling Language

Authors: Lukas Buchner; Philipp Zallinger; Karin Nachbagauer; Alois Zoitl; Roman Froschauer

Author Affiliations: Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; LIT CPS Lab, Johannes Kepler University, Linz, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria

Keywords:

Abstract: Programming human-robot collaboration (HRC) systems remains challenging for non-expert users. It often requires complex coding skills and provides limited visibility into robot behavior. We present the Robot Collaboration Language (RCL), a Gantt chart-based, domain-specific modeling language designed to facilitate intuitive and safe programming of collaborative tasks by non-experts. Using familiar Gantt chart representations, RCL aims to improve HRC programming transparency, predictability, and safety. We describe the language’s meta-model and implementation and demonstrate its use with an example. Our approach contributes to developing trustworthy HRC systems by simplifying the complexity of programming.

Publication: 2025 IEEE 21st International Conference on Automation Science and Engineering (CASE)

Year: 2025

ISSN: 2161-8070

ISBN: 979-8-3315-2247-6

DOI: 10.1109/CASE58245.2025.11164122

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11164122

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

## A Conceptual Modelling Language for CPPS

Authors: Mainak Majumder; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: CPPS; Domain Models; DSML; Production systems; Semantics; Green products; Manufacturing; Usability; Standards; Interoperability; Manufacturing automation; Software engineering; Software development management

Abstract: Semantic domain models are becoming an essential component of software-intensive Cyber-Physical Production Systems (CPPSs). They support the implementation of innovative concepts like Digital Twins (DTs), that enable autonomous operations of an entire production environment. However, developing domain models for CPPS is a challenging endeavour, especially due to a lack of standardised modelling approaches within the manufacturing domain. In this paper, we have tried to reduce this existing research gap by proposing a conceptual modelling approach that allows developing generic domain models of a production environment. The focus of this research work is to define generic modelling constructs that can be employed to capture domain concepts in a technology- or standard-neutral manner and used by various software engineering disciplines to develop diverse use case-specific CPPS applications.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205675

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205675

Publisher: IEEE

## Towards Event Flow Graphs for Analyzing Event Propagation in IEC 61499

Authors: Dunja Životin; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University, Linz, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria

Keywords: IEC 61499; Control Flow Graph; Event Flow Graph; Visualization; Runtime; Software algorithms; Model checking; Software; Maintenance; Flow graphs; IEC Standards; Standards; Manufacturing automation

Abstract: Understanding event propagation in IEC 61499 applications presents a significant challenge for control software developers. To address this issue, we adapted the well-known concept from software engineering called control flow graphs to create Event Flow Graphs. The purpose of developing Event Flow Graphs is to better understand and model event flow through IEC 61499 applications, and to see how the flow affects hardware and software components of the system. Our initial results show that Event Flow Graphs can accurately capture the properties of IEC 61499 models. This enables us to interpret common graph properties and invariants, and apply basic graph algorithms to query Event Flow Graphs efficiently. In addition, as an analysis tool, Event Flow Graphs represent a good alternative to visualize IEC 61499 applications, whose graphical and hierarchical nature can sometimes obscure event execution. The first findings indicate that Event Flow Graphs are valuable for analyzing and visualizing IEC 61499 software.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205700

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205700

Publisher: IEEE

## Modeling Interaction Patterns for Distributed Systems with IEC 61499

Authors: Peter Herrmann; Alois Zoitl

Author Affiliations: University of Science and Technology (NTNU), Trondheim, Norway; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords: Factory Automation Control System Development; IEC 61499; Interaction in Distributed Systems; Common Interaction Patterns; Upper bound; Heart beat; Prevention and mitigation; Computational modeling; Dynamic scheduling; Libraries; Fourth Industrial Revolution; Resource management; IEC Standards; Manufacturing automation

Abstract: IEC 61499 is a proven technique for the model-based engineering of factory automation systems. Due to recent developments in this field like Industry 4.0, however, modern systems rely more and more on distributed computer technology. In this article, we investigate if and to which degree IEC 61499 together with IEC 61131-3 Structured Text as the algorithm implementation language is suited to also model the behavior of these amended systems. To achieve that, we selected three relevant use cases, i.e., mixed initiative mitigation, free-pool, and heartbeat, and exemplarily implemented each of them. This allowed us to get insight about what can be conveniently specified using IEC 61499 and for what an extension of the modeling technique is recommended. In this paper, we introduce the models for the three use cases and report the lessons learned from their implementation. Based on that, we suggest enhancements to IEC 61499.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205734

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205734

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

## Offline Reproduction of Function Block Networks in IEC 61499 Resources

Authors: Jose Cabral; Alois Zoitl

Author Affiliations: Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria

Keywords: Replay debugging; time travel debugging; tracing; automation; IEC 61499; Analytical models; Runtime; Programmable logic devices; Debugging; Logic; IEC Standards; Observability; Machinery; Standards; Manufacturing automation

Abstract: The debugging capabilities in the automation domain lag behind those in other domains. One obstacle to debugging systems in the automation domain is the presence of heavy and costly machinery connected to the Programmable Logic Controllers (PLCs). Replay debugging presents an opportunity to overcome this issue by allowing the user to debug a system with full control and observability, without the real system being connected. During the first stage of replay debugging, information is captured while the system is running. This is then used during the second stage to reproduce the system in a safe environment.This work focuses on a viability analysis of replay debugging for Function Block networks within resources modelled according to the IEC 61499 standard. In order to reduce the execution impact of information capture, the work presents an approach where only a small subset of the run-time information is captured and can be used in an offline stage to generate the full execution behaviour of an IEC 61499 resource. Thorough tests and experiments show that the reproduction of the original states is possible.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205784

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205784

Publisher: IEEE

## Towards a Skill-Based Framework for User-Centric QoS-Based Orchestration of Human-Robot Collaboration Workflows

Authors: Lukas Buchner; Philipp Zallinger; Karin Nachbagauer; Alois Zoitl; Roman Froschauer

Author Affiliations: Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria

Keywords: Human-robot collaboration; Workflow modeling; Adaptive orchestration; Sequential analysis; Adaptive systems; Robot kinematics; Ergonomics; Human-robot interaction; Quality of service; Real-time systems; Energy efficiency; Planning; Middleware

Abstract: Human-Robot Collaboration (HRC) offers potential for flexible manufacturing, especially in small and medium-sized enterprises, but existing systems often lack adaptability to dynamic environments and human needs. This paper presents a novel, skill-based framework for user-centric, Quality of Service (QoS) based orchestration of HRC workflows. Our three-layer architecture separates non-real-time orchestration and workflow management from real-time, safety-critical execution, coordinated via a user-friendly interface using our Gantt chart-based Robot Collaboration Language. The framework allows users to define QoS goals (e.g., speed, energy efficiency, ergonomics), influencing high-level orchestration and low-level motion planning. This paper details the implementation and demonstrates the framework’s structure. It contributes towards more flexible, efficient, and human-aware robotic systems by providing an integrated approach to adaptive HRC workflow execution.

Publication: 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2025

ISSN: 1946-0740

ISBN: 979-8-3315-5384-5

DOI: 10.1109/ETFA65518.2025.11205791

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11205791

Publisher: IEEE

## Refactoring with Confidence: An Assistant for Repair-Integrated Refactoring in Block-based Industrial Models

Authors: Michael Oberlehner; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz; LIT CPS Lab, Johannes Kepler University Linz; LIT CPS Lab, Johannes Kepler University Linz

Keywords: Refactoring; Model repair; Industrial automation; Model maintenance; Industries; Visualization; Software maintenance; Automation; Software packages; Semantics; Maintenance engineering; Model driven engineering; Maintenance; IEC Standards

Abstract: When designing cyber-physical systems, especially in industrial automation, model-driven engineering plays an essential role in ensuring software maintainability and supporting evolution. Whereas textual programming environments provide mature tool support for refactoring and maintenance, equivalent capabilities in many industrial visual languages, such as IEC 61499 and Simulink, remain underdeveloped. This research addresses the challenges of maintaining and refactoring models in typed block-based modeling languages, such as IEC 61499 and Simulink, which are frequently used in industry. We propose a methodology that embeds repair mechanisms directly into refactoring processes, ensuring model consistency and minimizing manual intervention. By introducing a meta-model-based approach, we identify common maintenance operations and systematically define transformations that preserve the execution semantics while improving maintainability. Our approach is evaluated through a cross-language implementation, demonstrating its applicability across different modeling tools and industrial settings. We developed the concepts and assistance tools in close collaboration with our industry partner to enable software maintenance of large-scale automation software. The lessons learned are generalizable for various tool developers and contribute to error-resilient model evolution in visual modeling environments.

Publication: 2025 ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems (MODELS)

Year: 2025

ISSN:

ISBN: 979-8-3315-4911-4

DOI: 10.1109/MODELS67397.2025.00015

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11245365

Publisher: IEEE

## Identification of an Approach for the Execution of Skill-Based Domain-Specific Languages in the Area of Human-Robot Collaboration

Authors: Lukas Buchner; Philipp Zallinger; Karin Nachbagauer; Alois Zoitl; Roman Froschauer

Author Affiliations: Automation Engineering, University of Applied Sciences Upper Austria, Wels, Austria; Mechanical Engineering, University of Applied Sciences Upper Austria, Wels, Austria; Mechanical Engineering, University of Applied Sciences Upper Austria, Wels, Austria; LIT CPS Lab, Johannes Kepler University, Linz, Austria; Automation Engineering, University of Applied Sciences Upper Austria, Wels, Austria

Keywords: Domain-Specific Modeling; Domain-Specific Language; Human-Robot Collaboration; Robot kinematics; Human-robot interaction; Programming; Robot sensing systems; Sensors; DSL; Spatial resolution; Monitoring; Domain specific languages; Systematic literature review

Abstract: Domain-specific languages (DSLs) can simplify the programming of human-robot collaboration (HRC) systems for non-experts. However, executing skill-based DSLs for HRC programming requires integrating various production resources such as robots, humans, and sensors. Therefore, domain overlapping requirements must be considered when choosing an appropriate execution approach. This paper identifies and explains key requirements such as flexible interfaces, dynamic capability discovery, task dependency resolution, spatial awareness, continuous monitoring, and user interfaces. Through a comprehensive literature review and gap analysis, we identify trade-offs in execution methodologies. Based on this, we propose an orchestration-based strategy that offers centralized coordination, extendable interface integration, and monitoring capabilities to address current limitations in executing DSLs in HRC applications.

Publication: 2025 IEEE 23rd International Conference on Industrial Informatics (INDIN)

Year: 2025

ISSN: 1935-4576

ISBN: 979-8-3315-1122-7

DOI: 10.1109/INDIN64977.2025.11279180

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11279180

Publisher: IEEE

## Model-as-a-Middleware: Information Model as an Integrator for Cyber-Physical Production Systems

Authors: Mainak Majumder; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: CPPS; DSL; Information Model; OPC UA; Productivity; Production systems; Semantics; Manufacturing; Digital twins; DSL; Informatics; Artificial intelligence; Software engineering; Business

Abstract: Cyber-Physical Production Systems (CPPSs) have emerged as a cutting-edge manufacturing paradigm that aims to utilise innovative technological concepts like the Digital Twin and Artificial Intelligence to upgrade and optimise the productivity level of manufacturing environments. These concepts typically thrive on data and could be challenging to implement due to the semantic heterogeneity induced by the diverse manufacturing resources. Information modelling is a well-established approach traditionally used in software engineering to address semantic heterogeneity. Although the relevance of information modelling has already been established in CPPS, a suitable framework for information model development is not yet available. Therefore, our goal is to address this issue by proposing a domain-specific semantic information modelling framework for CPPS that enables the seamless integration of diverse manufacturing resources into intelligent business applications.

Publication: 2025 IEEE 23rd International Conference on Industrial Informatics (INDIN)

Year: 2025

ISSN: 1935-4576

ISBN: 979-8-3315-1122-7

DOI: 10.1109/INDIN64977.2025.11279640

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11279640

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

## Reactive Scheduling for Human-Robot Collaboration: An Event-Driven Approach with Adaptive Skill Execution

Authors: Lukas Buchner; Philipp Zallinger; Karin Nachbagauer; Alois Zoitl; Roman Froschauer

Author Affiliations: Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria; CDL VaSiCS; Faculty of Engineering and Environmental Sciences, University of Applied Sciences Upper Austria, Wels, Austria

Keywords: Human-robot collaboration; Reactive systems; Event-driven architecture; Robots; Printing; Timing; Modeling; Schedules; Scheduling; Finishing; Human-robot interaction; Joining processes; Programming

Abstract: Human-Robot Collaboration opens up new opportunities for small and medium-sized enterprises to meet the demands of mass customization while increasing productivity. However, these companies often lack robotics experts, so they need programming approaches that non-experts can understand. To address this, we previously introduced the Robot Collaboration Language (RCL), a skill-based visual Domain-Specific Language that models workflows as Gantt charts. The execution of such a Gantt-modeled workflow, however, comes with its own challenges. As human timing fluctuates during execution, the temporal constraints between tasks modeled in RCL can only be honored if the schedule is continuously updated and propagated as work progresses. To address these challenges, an event-driven architecture is presented that combines three core mechanisms: a decomposition algorithm based on strongly connected components to detect cyclic temporal dependencies; a linear programming adaptive scheduling to enable feasible time adjustments while accounting for ongoing tasks; and a reactive execution strategy that propagates updates throughout execution. This approach enables a seamless synchronization between human and robot, providing an execution framework that remains robust under real-world temporal uncertainty.

Publication: 2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2026

ISSN: 1946-0740

ISBN: 979-8-3315-7889-3

DOI: 10.1109/ETFA68377.2026.11724823

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11724823

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

## Environment-Aware Event Flow Graphs for IEC 61499 Applications

Authors: Dunja Životin; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Austria; CDL VaSiCS

Keywords: IEC 61499; event propagation; environment; Modeling; Synchronization; IEC; Sequences; Sequential analysis; Labeling; Printing; Flow graphs; Technology; Timing

Abstract: We previously proposed the Event Flow Graph (EFG), a model for analyzing and visualizing event propagation in IEC 61499 application models. While the original approach handles certain Function Blocks well, its expressiveness for SIFBs is limited. Without accounting for the environment boundaries and the synchronization between input events, EFGs either underspecify reachable paths based on the limited service sequences available, or they over-approximate them by falling back on an all-to-all mapping. We extend EFGs with two new structural elements. The first one is a synchronization state that represents the point at which the input events of a Function Block must synchronize before continuing execution. The second contribution is the gated edge, which represents the boundary between the application and its environment. We demonstrate the extension using SIFBs defined in the standard: Requester, Responder, and E_DELAY. Furthermore, we update the definitions of root nodes and dependency edges from our previous work.

Publication: 2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2026

ISSN: 1946-0740

ISBN: 979-8-3315-7889-3

DOI: 10.1109/ETFA68377.2026.11725077

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11725077

Publisher: IEEE

## Towards Data Dependence Graphs for IEC 61499 Basic Function Blocks

Authors: Dunja Životin; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University, Linz, Austria; CDL VaSiCS, Johannes Kepler University, Linz, Austria

Keywords: IEC 61499; Data Dependence Graphs; IEC; Algorithms; Modeling; Printing; Clamps; Elliptic curve cryptography; Error correction codes; Programming; Conferences

Abstract: Understanding some parts of IEC 61499 can be challenging. It requires careful dissection and interpretation of the standard to correctly capture its intended and desirable behavior. One of the main struggles lies in inspecting data dependence within function blocks. This is due to the combination of different components, ranging from an internal state machine and its algorithms to events associated to data, which can confuse even the best of control software developers. To address and improve this, our work introduces Data Dependence Graphs (DDGs) for IEC 61499 Basic Function Blocks (BFBs) to capture data dependences in control software. The data dependence is built by deriving define/use relationships from the Structured Text algorithms, and by partially addressing the ordering of their executions when traversing the internal state machine. This is presented on an illustrative BFB, and is discussed in more detail, further hinting at the importance of static analysis for IEC 61499. Finally, the paper discusses limitations and outlines future work to extend the approach to other FB types.

Publication: 2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2026

ISSN: 1946-0740

ISBN: 979-8-3315-7889-3

DOI: 10.1109/ETFA68377.2026.11725294

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11725294

Publisher: IEEE

## Development, implementation and use of an IEC 61499 function block library for embedded closed loop control

Authors: T. Strasser; F. Auinger; A. Zoitl

Author Affiliations: Thomas Strasser and Franz Auinger, PROFACTOR Produktionsforschungs GmbH, Steyr, Austria; Thomas Strasser and Franz Auinger, PROFACTOR Produktionsforschungs GmbH, Steyr, Austria; Alois Zoitl, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: A wide range of industrial processes and applications are controlled by closed loop control systems. Such processes consist of the plant that needs to be controlled and of controlling elements such as actuators, sensors, regulators or controllers. Due to decreasing hardware costs controllers are more and more integrated into sensors, actuators or other field devices. The result is increased modularity, scalability and more intelligence of the control networks that can be built out of these new mechatronic devices. To be able to program such systems in a convenient and intuitive way the function block (FB) oriented IEC 61499 standard for modeling and engineering of distributed industrial process measurement and control systems was developed. First prototypes were successfully applied to the area of distributed discrete controllers. For the area of closed loop control there seems to be a natural link between block diagram descriptions of closed loop control elements and the FB concepts of IEC 61499. But up to now efforts for mapping and implementing the wide range of block diagram element of closed loop control theory to IEC 61499 constructs were outstanding. The goal of this paper is to investigate the possibilities for applying the concept of the IEC 61499 standard to the field of closed loop control. Therefore, computer aided design and engineering tools for closed loop control systems that are currently used by control engineers for design and control of centralized automatic control systems are analyzed regarding their capabilities. Based on this information, new FB types are identified to cover the core functionality that is necessary for the implementation in closed loop control systems. Based on this analysis a library of FB types for closed loop control applications was developed and applied. The usage and limitations of IEC 61499 for distributed closed loop control is demonstrated on a real experiment - the control of a challenging seesaw problem

Publication: 2nd IEEE International Conference on Industrial Informatics, 2004. INDIN '04. 2004

Year: 2004

ISSN:

ISBN: 0-7803-8513-6

DOI: 10.1109/INDIN.2004.1417415

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1417415

Publisher: IEEE

## Dynamic reconfiguration of distributed control applications with reconfiguration services based on IEC 61499

Authors: Alois Zoitl; Christoph Sunder; Ivanka Terzic

Author Affiliations: Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria

Keywords:

Abstract: The support of dynamic reconfiguration on all automation levels of future manufacturing systems will the the key success factor of agile production systems. Up to now the main hindering point is the lacking support on the lowest - the real-time control - level. This work identifies requirements a dynamic reconfigurable control architecture has to fulfil. It derives a set of basic reconfiguration services based on general reconfiguration tasks. These basic services can be arbitrarily arranged to sequences accomplishing the reconfiguration process. The infrastructure presented in this paper will serve as basis for next generation self adapting agile manufacturing systems

Publication: IEEE Workshop on Distributed Intelligent Systems: Collective Intelligence and Its Applications (DIS'06)

Year: 2006

ISSN:

ISBN: 0-7695-2589-X

DOI: 10.1109/DIS.2006.28

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1633427

Publisher: IEEE

## Knowledge-based Multi-agent Architecture

Authors: Munir Merdan; Vedran Kordic; Alois Zoitl; Aleksandar Lazinica

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Austria; Automation and Control Institute, Vienna University of Technology, Austria; Automation and Control Institute, Vienna University of Technology, Austria; Vienna University of Technology, Institute of Production Engineering, Austria

Keywords:

Abstract: This paper presents a knowledge-intensive multi-agent architecture that enables ontology-based communication and cooperation among a set of autonomous and heterogeneous agents. An agent, the main core of our architecture, acts based on his knowledge, by sensing the manufacturing environment, triggering the reasoning process, which selects the proper actions to be executed and that will affect the manufacturing environment. The ontology is shared among agents and serves as the instrument to define the vocabulary used by the agents during their interactions, and to support "understanding" of the message content in the sense of its correct interpretation.

Publication: 2006 International Conference on Computational Inteligence for Modelling Control and Automation and International Conference on Intelligent Agents Web Technologies and International Commerce (CIMCA'06)

Year: 2006

ISSN:

ISBN: 0-7695-2731-0

DOI: 10.1109/CIMCA.2006.140

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4052699

Publisher: IEEE

## Usability and Interoperability of IEC 61499 based distributed automation systems

Authors: Christoph Sunder; Alois Zoitl; James H. Christensen; Valeriy Vyatkin; Robert W. Brennan; Antonio Valentini; Luca Ferrarini; Thomas Strasser; Jose L. Martinez-lastra; Franz Auinger

Author Affiliations: Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria; Holobloc Inc., Cleveland Heigths, OH, USA; Dept. of Electrical and Computer Engineering, The University of Auckland, Auckland, New Zealand; Schulich School of Engineering, University of Calgary, Calgary, Alberta, Canada; Centro di Ricerca e Innovazione Tecnologica Crit Srl, Vignola (Mo), Italy; Dipartimento di Elettronica e Informazione Politecnico di Milano, Milano, Italy; Robotics and Adaptive Systems, PROFACTOR Produktionsforschungs GmbH, Steyr-Gleink, Austria; Institute of Production Engineering, Tampere University of Technology, Tampere, Finland; Upper Austrian University of Applied Science, Automation Engineering University of Applied Science, Wels, Austria

Keywords:

Abstract: Since IEC 61499 has reached the state of an International Standard and a substantial body of research results exists the question of the authors as main intention for this paper was: Do the models of IEC 61499 solve all problems when thinking of usability and interoperability in heterogeneous system environments? The main problems discussed within the paper concern to the execution model defined for basic function blocks and the scheduling of events within function block networks.

Publication: 2006 4th IEEE International Conference on Industrial Informatics

Year: 2006

ISSN: 2378-363X

ISBN: 0-7803-9700-2

DOI: 10.1109/INDIN.2006.275713

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4053358

Publisher: IEEE

## Considering IEC 61131-3 and IEC 61499 in the context of component frameworks

Authors: Christoph Sunder; Alois Zoitl; James H. Christensen; Heinrich Steininger; Josef Rritsche

Author Affiliations: Vienna University of Technology, Vienna, Austria; Technische Universitat Wien, Wien, Wien, AT; Holobloc Inc. Cleveland, Ohio, USA; Logi.cals Austria-kirchner SOFT GmbH, Austria; Bachmann electronic GmbH, Kreuzäckerweg 33, 6800 Reldkirch-Tosters, Austria

Keywords:

Abstract: Automation and control systems provide their own programming and modeling paradigms in parallel to theory well known from computer science. Especially the concepts of component-based software engineering highly influence the design of embedded systems, which include automation and control systems. This work analyses what is and is not a “software component” in the context of the two standards IEC 61131-3 and IEC 61499. Utilizing the definition of component frameworks and component system architectures, the potentials and problems of an integrative approach in order to utilize both standards within the same platform will be discussed.

Publication: 2008 6th IEEE International Conference on Industrial Informatics

Year: 2008

ISSN: 2378-363X

ISBN: 978-1-4244-2171-8

DOI: 10.1109/INDIN.2008.4618109

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4618109

Publisher: IEEE

## Framework for Distributed Industrial Automation and Control (4DIAC)

Authors: Thomas Strasser; Martijn Rooker; Gerhard Ebenhofer; Alois Zoitl; Christoph Sunder; Antonio Valentini; Allan Martel

Author Affiliations: PROFACTOR GmbH, Austria; PROFACTOR GmbH, Austria; PROFACTOR GmbH, Austria; Automation and Control Institute (ACIN), Odo-Struger Lab, Vienna University of Technology, Vienna, Austria; Automation and Control Institute (ACIN), Odo-Struger Lab, Vienna University of Technology, Vienna, Austria; O3NEIDA Inc., Ottawa, ONT, Canada; O3NEIDA Inc., Ottawa, ONT, Canada

Keywords:

Abstract: This paper intends to provide a basis for the discussion and development of an Open Source Initiative for a “Framework for Distributed Industrial Automation and Control (4DIAC) based on the new IEC 61499 standard. The general understanding of the authors is that an open source strategy is an adequate means for pushing current developments within the industrial automation domain and bringing together interested partners to focus and unite their concerns on a distributed and flexible automation environment. One main point is also to provide a stable basis for industrial appliances and further research into next generation distributed automation and control systems based on the IEC 61499 standard. A look at the current status of the developments for IEC 61499 shows, that these targets may not have been attained. In the opinion of the authors, the targets presented above need a common and publicly available reference framework. Therefore the general idea of the 4DIAC initiative is to provide such an open framework for the IEC 61499 standard that gives the opportunity to establish an automation and control environment based on the three main targets, portability, configurability and interoperability.

Publication: 2008 6th IEEE International Conference on Industrial Informatics

Year: 2008

ISSN: 2378-363X

ISBN: 978-1-4244-2171-8

DOI: 10.1109/INDIN.2008.4618110

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4618110

Publisher: IEEE

## Knowledge-based multi-agent architecture for dynamic scheduling in manufacturing systems

Authors: Munir Merdant; Pavel Vrba; Gottfried Koppensteiner; Alois Zoitl

Author Affiliations: Automation and Control Institute (ACIN), Vienna University of Technology, Gusshausstrasse 27-29/E376, A-1040 Vienna, Austria; Rockwell Automation Research Center, Prague, Czech Republic; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: The scheduling of production resources is one of the key features in the current competitive and dynamic manufacturing environment. The scheduling has to be flexible and able to cope with conflicts derived from the resources sharing among the production orders. We present a knowledge-based multi-agent approach combined with negotiation mechanisms for task allocation as a preliminary step towards optimized scheduling. We explained the scheduling strategy, where each agent performs local scheduling using dispatching rules and coordinates its actions with other agents optimizing at the same time global dynamic scheduling of the manufacturing system. An ontology is used to support ldquounderstandingrdquo between agents during the communication, as well as to explicitly define the domain entities and relations between them.

Publication: 2008 6th IEEE International Conference on Industrial Informatics

Year: 2008

ISSN: 2378-363X

ISBN: 978-1-4244-2171-8

DOI: 10.1109/INDIN.2008.4618262

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4618262

Publisher: IEEE

## Structuring of large scale distributed control programs with IEC 61499 subapplications and a hierarchical plant structure model

Authors: Thomas Strasser; Martijn Rooker; Gerhard Ebenhofer; Alois Zoitl; Christoph Sunder; Antonio Valentini; Allan Martel

Author Affiliations: PROFACTOR GmbH, Steyr Gleink, Austria; PROFACTOR GmbH, Steyr Gleink, Austria; PROFACTOR GmbH, Steyr Gleink, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; O3neida Europe Asbl, Brussels, Belgium; O3neida Europe Asbl, Brussels, Belgium

Keywords:

Abstract: The automation of plants and machines is becoming more and more complex due to the extensive usage of intelligent field devices as for instance programmable actuators and sensors. The graphical programming languages used are typically for the automation domain, and control applications tend to be become increasingly complex which results in higher engineering costs for establishment and maintenance. The new IEC 61499 standard for distributed control systems provides an interesting engineering concept called subapplications. This concept has, in principle, the potential to provide a cost-effective solution for industrial automation applications, but is currently only being used in a few instances. The goal of this paper is to introduce a simpler, more effective, engineering approach to structure large scale distributed control programs based on a hierarchical plant structure model together with IEC 61499 subapplications.

Publication: 2008 IEEE International Conference on Emerging Technologies and Factory Automation

Year: 2008

ISSN: 1946-0759

ISBN: 978-1-4244-1506-9

DOI: 10.1109/ETFA.2008.4638507

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4638507

Publisher: IEEE

## Improving Component Testing of Industrial Automation Software

Authors: Harald Krapfenbauer; Dominik Ertl; Alois Zoitl; Friederich Kupzog

Author Affiliations: Institute of Computer Technology, Vienna University of Technology, Vienna, Austria; Institute of Computer Technology, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Institute of Computer Technology, Vienna University of Technology, Vienna, Austria

Keywords: Industrial Automation Software; IEC 61499; Component Testing; Dynamically Typed Languages; Automatic testing; Software testing; Computer industry; Automation; System testing; Electronic equipment testing; IEC standards; Hardware; Industrial control; Industrial electronics

Abstract: Industrial automation systems are tested nowadays mainly via system tests at a very late stage of development. These tests are conducted manually, are time-consuming and cost-intensive. Earlier testing of automation software, e.g., component testing, is therefore desired in order to reduce the effort for system testing by detecting errors sooner. In this paper we present an improved concept for a test environment that enables developers of industrial control electronics to test the functionality of IEC 61499 software components. Components can be tested on any hardware with an IEC 61499 runtime environment, even on the target hardware. There is no need to change the automation software for testing. We propose using dynamically typed languages to implement tests because such languages have inherent properties that are useful for this task. We provide example code of a typical test case.

Publication: 2009 Fourth International Multi-Conference on Computing in the Global Information Technology

Year: 2009

ISSN:

ISBN: 978-0-7695-3751-1

DOI: 10.1109/ICCGI.2009.46

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5280052

Publisher: IEEE

## Is IEC 61499 in harmony with IEC 61131-3?

Authors: Alois Zoitl; Thomas Strasser; Christoph Sunder; Thomas Baier

Author Affiliations: Electrical engineering, Control technology, University of Technology, Vienna, Austria; Mechanical engineering, Control technology, University of Technology, Vienna, Austria; ACIN; Vienna University of Technology, Austria

Keywords:

Abstract: This year marks the 16th anniversary of the International Electrotechnical Commission (IEC) 1131-3 (now IEC 61131-3), currently one of the most important standards in industrial automation. Four years before its release, it has been decided that it will define a further standard for programming industrial control systems, the IEC 61499 standard. One reason for this decision has been the remarkable, and still current study, of the Iacocca Institute [ 1 ]. This study identified: portability-software tools can accept and correctly interpret software components and system configurations produced by other software tools; interoperability-embedded devices can operate together to perform the functions needed for distributed applications; configurability-any device and its software components can be configured by software tools from multiple vendors; reconfiguration-the ability to adapt control hardware and software during operation; distribution-the ability to distribute software components onto different hardware devices, as requirements demanded from future industrial process measurement and control systems (IPMCS) by the automation industry.

Publication: IEEE Industrial Electronics Magazine

Year: 2009

ISSN: 1941-0115

ISBN:

DOI: 10.1109/MIE.2009.934797

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5352484

Publisher: IEEE

## Different perspectives [Face to face; "IEC 61499 architecture for distributed automation: The `"glass half full" view]

Authors: Alois Zoitl; Valeriy Vyatkin

Author Affiliations: Vienna University of Technology, Austria; University of Auckland, New Zealand

Keywords:

Abstract:

Publication: IEEE Industrial Electronics Magazine

Year: 2009

ISSN: 1941-0115

ISBN:

DOI: 10.1109/MIE.2009.934789

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5353084

Publisher: IEEE

## Toward Self-Reconfiguration of Manufacturing Systems Using Automation Agents

Authors: Wilfried Lepuschitz; Alois Zoitl; Mathieu Vallée; Munir Merdan

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Institute of Computer Technology, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords: Automation agent; flexible manufacturing; IEC 61499; low-level control (LLC); ontology; reconfiguration; Automation; Manufacturing systems; Computer architecture; Software; IEC standards; Real time systems

Abstract: The reconfiguration of control software is regarded as an important ability to enhance the effectiveness and efficiency in future manufacturing systems. Agent technology is considered as a promising approach to provide reconfiguration abilities, but existing work has been focused mainly on the reconfiguration of higher layers concerned with production scheduling and planning. In this paper, we present an automation agent architecture for controlling physical components that integrates “on the fly” reconfiguration abilities on the low-level layer. Our approach is combined with an ontological representation of the low-level functionality at the high-level control layer, which is able to reason and initiate reconfiguration processes to modify the low-level control (LLC). As current control systems are mostly based on standards and principles that do not support reconfiguration, leading to rigid control software architectures, we base our approach on the promising Standard IEC 61499 for the LLC, extended by an innovative reconfiguration infrastructure. We demonstrate this approach with a case study of a reconfiguration process that modifies the LLC functionality provided by the automation agent of a physical component. Thereby, we obtain the ability to support numerous different LLC configurations without increasing the LLC's complexity. By applying our automation agent architecture, we enhance not only the flexibility of each component's control software, but also achieve the precondition for reconfiguring the entire manufacturing system.

Publication: IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews)

Year: 2011

ISSN: 1558-2442

ISBN:

DOI: 10.1109/TSMCC.2010.2059012

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5557828

Publisher: IEEE

## Design and Execution Issues in IEC 61499 Distributed Automation and Control Systems

Authors: Thomas Strasser; Alois Zoitl; James H. Christensen; Christoph Sünder

Author Affiliations: AIT Austrian Institute of Technology, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Holobloc Inc., Cleveland Heights, Cleveland Heights, OH, USA; Thales Rail Signalling Solutions GesmbH, Vienna, Austria

Keywords: Distributed control system; Holonic Manufacturing System (HMS); IEC 61499; lower level control approach; IEC standards; Automation; Real time systems; Software; Control systems; Manufacturing; Context

Abstract: The standard IEC 61499 claims to be a standard for a distributed control environment consisting of a set of heterogeneous control devices from different vendors. Previous work on the implementation of IEC 61499 pointed out ambiguities in the standard, resulting in different execution behavior of IEC 61499 elements on different control devices. One of the key deficiencies is the lack of a definition for execution models of the device, the resource, and the function blocks. This paper discusses different design and execution issues related to the aforementioned problems for IEC 61499 distributed automation and control systems.

Publication: IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews)

Year: 2011

ISSN: 1558-2442

ISBN:

DOI: 10.1109/TSMCC.2010.2067210

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5571034

Publisher: IEEE

## Online reconfiguration of the low level control for automation agents

Authors: Wilfried Lepuschitz; Mathieu Vallée; Alois Zoitl; Munir Merdan

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Institute of Computer Technology, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Addressing changing market conditions and customer needs requires more flexible and reconfigurable manufacturing systems. Distributed intelligent control systems based on agent technologies are seen as a promising approach to provide reconfiguration abilities. Existing work has been focused on the reconfiguration of higher layers concerned with production planning and scheduling. However, a different approach is needed for reconfiguration of the control software at a lower level closer to physical components, in order to enable a better adaptation to changes and disturbances in the local environment. In this paper, we investigate the feasibility of online reconfiguration of the low level control for automation agents. Our approach relies on a reconfiguration infrastructure for real-time control software based on the IEC 61499 standard. We detail the features of this infrastructure as well as its integration within the architecture of an automation agent. We also describe an implementation example with timing measurements showing the ability for rapid reconfiguration. Using our approach, reconfiguration can be performed locally without the need to restart the control system.

Publication: IECON 2010 - 36th Annual Conference on IEEE Industrial Electronics Society

Year: 2010

ISSN: 1553-572X

ISBN: 978-1-4244-5226-2

DOI: 10.1109/IECON.2010.5675483

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5675483

Publisher: IEEE

## Building hierarchical automation solutions in the IEC 61499 modeling language

Authors: Alois Zoitl; Herbert Prähofer

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; CD Laboratory for Automated Software Engineering, Institute for System Software, Johannes Kepler University, Linz, Austria

Keywords:

Abstract: The IEC 61499 modeling language pursues a component-based approach with modular building blocks coupled by ports and arranged in a hierarchical manner. However, as in similar approaches, the IEC 61499 language does not define how functional hierarchies of upper- and lower-level functional entities should be built. In this paper, motivated by our previous work, structuring principles for IEC 61499 for purely hierarchical control solutions are presented. We present elementary design guidelines for structuring automation solutions in several hierarchical layers, outline which elements of IEC 61499 to use, and illustrate the approach by an architecture for an example control system.

Publication: 2011 9th IEEE International Conference on Industrial Informatics

Year: 2011

ISSN: 2378-363X

ISBN: 978-1-4577-0433-8

DOI: 10.1109/INDIN.2011.6034940

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6034940

Publisher: IEEE

## Utilizing IEC 61499 in an MDA control application development approach

Authors: Monika Wenger; Martin Melik-Merkumians; Ingo Hegny; Reinhard Hametner; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Traditional control application engineering techniques tend to mix logical functionality with hardware access methods. This greatly impedes reusability. Through separation of the logical control application domain and the specific hardware domain the MDA (Model-Driven Architecture) proposes a solution to this problem. In the domain of embedded systems development this approach brought a great advantage in reducing the complexity of the development process. In this paper we investigate if and how IEC 61499 can be utilized as a DSL (Domain Specific Language) for control application development in the domain of industrial automation systems. We will show the potentials of our work by developing a sample control application using the suggested methods.

Publication: 2011 IEEE International Conference on Automation Science and Engineering

Year: 2011

ISSN: 2161-8070

ISBN: 978-1-4577-1731-4

DOI: 10.1109/CASE.2011.6042458

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6042458

Publisher: IEEE

## Distributed online change for IEC 61499

Authors: Andreas Schimmel; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Future automation systems exhibit a growing demand for downtimeless evolution. There have been already several approaches for this so called online change but most of them are manly designed to work within a device. The increasing distribution of automation systems needs an efficient mechanism for downtimeless reconfiguration even if the change affects more devices. So this paper will show an approach how this distributed online change can be done for IEC 61499 systems. Distributed reconfiguration needs a synchronisation of the involved devices which will be done in this approach by synchronised clocks. The basis for this paper builds an existing approach for downtimeless reconfiguration (eCEDAC-Approach) which will be extended to get an efficient mechanism for distributed online change.

Publication: ETFA2011

Year: 2011

ISSN: 1946-0740

ISBN: 978-1-4577-0016-3

DOI: 10.1109/ETFA.2011.6059117

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6059117

Publisher: IEEE

## Improved communication model for an IEC 61499 runtime environment

Authors: M. Hofmann; Martijn Rooker; Alois Zoitl

Author Affiliations: Profactor GmbH, Steyr-Gleink, Austria; Profactor GmbH, Steyr-Gleink, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: For IEC 61499 distributed control application development the control engineer has to rely mainly on the Compliance Profile for Feasibility Demonstrations for the necessary communication infrastructure. This profile utilizes the TCP/UDP protocols and has some limitations in order to be easily used for industrial automation. With this article we identify these shortcomings and introduce an improved communication model for IEC 61499 control applications. The following three attempts to define communication interaction in IEC 61499 will be presented: (1) by function block type defined protocol, (2) by function block parameter defined protocol, (3) automatic connection. We show the impact of these attempts from the engineer's point of view. Also the required engineering tool features are presented. The result is a profile which enables the engineer to easily use different network protocols within IEC 61499 applications without the limitation to use only the TCP/UDP protocol. Furthermore, this paper shows the implementation of the developed communication profile. The implementation focuses on the runtime environment and shows how the implementation can be used by the engineer and by the engineering tool. The implementation takes strong attention to the re-usability of already implemented protocols. This is achieved by the usage of the ”layered protocol” design pattern.

Publication: ETFA2011

Year: 2011

ISSN: 1946-0740

ISBN: 978-1-4577-0016-3

DOI: 10.1109/ETFA.2011.6059121

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6059121

Publisher: IEEE

## Engineering process for an online testing process of control software in production systems

Authors: Benjamin Kormann; Birgit Vogel-Heuser; Reinhard Hametner; Alois Zoitl

Author Affiliations: Automation and Information Systems (AIS), Technische Universität München, Garching, Germany; Automation and Information Systems (AIS), Technische Universität München, Garching, Germany; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: An increasing number of functionality in today's machine and plant automation is being shifted from pure mechanics or electronics into software. Therefore the system behavior must be checked for compliance with the demanded software functionality by software tests. The precondition for test case execution is a start state, the system has to take in. In order to evaluate the testability of a system, it must be verified whether the test case triggering system state is reachable. We propose a transformation approach of the control software model and the corresponding environment model (physics) to timed automata for model checking to exploit the power of the query language Timed Computation Tree Logic for start state reachability analysis. The applicability is demonstrated on a laboratory plant.

Publication: ETFA2011

Year: 2011

ISSN: 1946-0740

ISBN: 978-1-4577-0016-3

DOI: 10.1109/ETFA.2011.6059205

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6059205

Publisher: IEEE

## Industrial embedded model predictive controller platform

Authors: Monika Wenger; Reinhard Hametner; Alois Zoitl; Andreas Voigt

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; VOIGTWIPP Engineers GmbH, Vienna, Austria

Keywords:

Abstract: Operating industrial plants at their maximum energy and resources efficiency often means to operate them close at their design limits. Due to strict safety and process parameter constraints, it is challenging to control them close to the optimal setpoints. Currently process performance improvement projects are realized by application of PC based model predictive controllers as add-ons. Applications of up-to-date optimizing control algorithms are characterized by high requirements on software architecture, numerical computing power and realtime behavior. These requirements are not accomplishable running optimizing control algorithms on Programmable Logic Controllers (PLCs) by current available software architectures. Therefore the aim of the Embedded Energy Efficiency Industrial Controller Platform (E3ICP) project is the development of an infrastructure for running state-of-the-art model predictive controllers on industrial embedded PLCs.

Publication: ETFA2011

Year: 2011

ISSN: 1946-0740

ISBN: 978-1-4577-0016-3

DOI: 10.1109/ETFA.2011.6059212

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6059212

Publisher: IEEE

## Ontology-driven automated software configuration for manufacturing system components

Authors: Wilfried Lepuschitz; Alois Zoitl; Munir Merdan

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords: Automation agent; automated configuration; ontology; IEC 61499; manufacturing system; Ontologies; Automation; Software; Switches; Sensors; IEC standards

Abstract: Nowadays the design and configuration of control applications is traditionally done manually once for a designated system layout. Manufacturing components, which autonomously embed themselves into the existing control system without requiring extensive human involvement, are regarded as vitally important to achieve more flexible and reconfigurable manufacturing systems. In this paper we investigate the feasibility of an automated configuration of the hardware-near control application for physical manufacturing components based on agent technology. We employ automation agents, which have an ontological representation of the physical components they control. Based on this knowledge, the agents use a reconfiguration infrastructure for control software based on the standard IEC 61499. Using our approach, the hardware-near control application does not have to be designed and instantiated manually as this is performed automatically.

Publication: 2011 IEEE International Conference on Systems, Man, and Cybernetics

Year: 2011

ISSN: 1062-922X

ISBN: 978-1-4577-0651-6

DOI: 10.1109/ICSMC.2011.6083703

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6083703

Publisher: IEEE

## Test case generation approach for industrial automation systems

Authors: Reinhard Hametner; Benjamin Kormann; Birgit Vogel-Heuser; Dietmar Winkler; Alois Zoitl

Author Affiliations: Automation and Control Institute (ACIN), Vienna University of Technology, Austria; Automation and Information Systems (AIS), Technische Universität München, Germany; Automation and Information Systems (AIS), Technische Universität München, Germany; CDL for Software Engineering Integration for Flexible Automation Systems, Vienna University of Technology, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Austria

Keywords:

Abstract: The need for increasing flexibility of industrial automation system products leads to the trend to shift functional behavior from hardware solutions to software components. This trend causes an increasing complexity of software components and the need for comprehensive and automated testing approaches to ensure a requested quality level. Nevertheless, a key task in software testing is to identify appropriate test cases typically requiring high effort for test case generation and rework effort for adapting test cases in case of requirements changes. Semi-automated derivation of test cases based on models, like UML, can support test case generation. In this paper we introduce an automated test case generation approach for industrial automation applications which are specified by UML state chart diagrams. In addition we present a prototype application of the presented approach for a sorting machine. Major results showed that state charts (a) can support efficient test case generation and (b) enable automated code generation of test cases and code for the industrial automation domain.

Publication: The 5th International Conference on Automation, Robotics and Applications

Year: 2011

ISSN:

ISBN: 978-1-4577-0328-7

DOI: 10.1109/ICARA.2011.6144856

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6144856

Publisher: IEEE

## IEC 61131-3 model for model-driven development

Authors: Monika Wenger; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Existing industrial automation projects require automated methods for faster changes and updates as well as continuous improvement and maintenance. Software Engineering uses Model Driven Development to shorten the development time by keeping documentation, models and code consistent during the whole development time and by using code generators to create many similar code artifacts and code for different platforms. To make this concept also available for automation projects we present an IEC 61131 model based on the Extended Backus Naur From provided by the standard. For the proposed IEC 61131 model also related application areas are outlined.

Publication: IECON 2012 - 38th Annual Conference on IEEE Industrial Electronics Society

Year: 2012

ISSN: 1553-572X

ISBN: 978-1-4673-2420-5

DOI: 10.1109/IECON.2012.6389295

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6389295

Publisher: IEEE

## Agile testing concepts based on keyword-driven testing for industrial automation systems

Authors: Reinhard Hametner; Dietmar Winkler; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Institute of Software Technology and Interactive Systems, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords: Industrial Control Applications; IEC 61131-3; IEC 61499; Test Automation; Keyword-driven Test; Force

Abstract: In the field of industrial automation systems software becomes an important factor because engineers tend to move the realization of functional requirements from hardware to software components. The main reason for this is that software components allow increasing product flexibility. As a consequence software complexity increases rapidly and requires systematic, automation-supported and agile testing approaches. Thus, systematic and agile testing are key challenges in industrial control software development to ensure and improve systems quality. Further different implementation standards, i.e., IEC 61131-3 and IEC 61499, arise additional challenges in constructing and testing industrial automation systems software. This paper presents an agile and keyword-driven test approach with focus on testing implementations based on both important industrial standards and illustrates the applicability of the purposed approach in a sample implementation, i.e., a High Speed Pick and Place unit. Main results show the applicability of keyword-driven testing based on a defined subset of keywords (common for IEC 61131-3 and IEC 61499) and thus enable agile and automation-supported testing more effective and efficient.

Publication: IECON 2012 - 38th Annual Conference on IEEE Industrial Electronics Society

Year: 2012

ISSN: 1553-572X

ISBN: 978-1-4673-2420-5

DOI: 10.1109/IECON.2012.6389298

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6389298

Publisher: IEEE

## A reconfigurable communication gateway for distributed embedded control systems

Authors: Filip Andrén; Thomas Strasser; Alois Zoitl; Ingo Hegny

Author Affiliations: Electric Energy Systems-Energy Department, AIT Austrian Institute of Technology GmbH, Vienna, Austria; Electric Energy Systems-Energy Department, AIT Austrian Institute of Technology GmbH, Vienna, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria; Automation and Control Institute (ACIN), Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Modern automation and control systems used in industrial large-scale applications are characterized by its distributed nature in the areas of power and energy systems, manufacturing, building automation, and logistics. In order to cope with different communication needs and changing requirements in such large-scale scenarios over its life-time, the main aim of this paper is to propose a programmable and (re-)configurable communication gateway device compliant to domain standards. This approach is therefore based on the IEC 61499 reference model for distributed and reconfigurable automation and uses the service interface function block concept and highlevel communication patterns to achieve a hardware-independent access to communication services. Moreover, the utilization of the IEC 61499 management model supports the possibility of the online-reconfiguration of communication links and therefore provides a very flexible structure and implementation for an industrial automation gateway device.

Publication: IECON 2012 - 38th Annual Conference on IEEE Industrial Electronics Society

Year: 2012

ISSN: 1553-572X

ISBN: 978-1-4673-2420-5

DOI: 10.1109/IECON.2012.6389299

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6389299

Publisher: IEEE

## Guidelines and Patterns for Building Hierarchical Automation Solutions in the IEC 61499 Modeling Language

Authors: Alois Zoitl; Herbert Prähofer

Author Affiliations: Fortiss GmbH, Munich, Germany; Institute for System Software, Johannes Kepler University of Linz, Linz, Austria

Keywords: Design guidelines; hierarchical software systems; IEC 61499; software architecture; IEC standards; Unified modeling language; Guidelines; Automation; Software architecture

Abstract: The IEC 61499 modeling language pursues a component-based approach with modular building blocks coupled by ports and arranged in a hierarchical manner. Like similar approaches, the IEC 61499 language does not define how functional hierarchies of upper- and lower-level functional entities should be built. In this paper we outline structuring principles for IEC 61499 programs with purely hierarchical control architectures. We present elementary design guidelines for structuring automation solutions in several hierarchical layers, outline which elements of the IEC 61499 language to use, discuss patterns that arise when implementing hierarchical control solutions, and illustrate the approach with a case study.

Publication: IEEE Transactions on Industrial Informatics

Year: 2013

ISSN: 1941-0050

ISBN:

DOI: 10.1109/TII.2012.2235449

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6389773

Publisher: IEEE

## Implementation of an event-based low-level control for mobile robots

Authors: Gottfried Koppensteiner; Christian Schwingenschlögl; Munir Merdan; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: Mobile robots get increasingly important in the implementation of adaptive production systems. In order to gain the most benefit from mobile robots they need at the one hand efficiently cooperate with the overall production system and on the other hand provide their functionality (e.g., pick and place of parts) fast and with a high precision. Semantic enhanced multi-agent systems have proven to serve well for the first task, especially in heterogeneous environments. However, they lack when applied to directly control automation equipment. In order to overcome this limitation this work presents an underlying low-level control architecture that takes over the task of handling the mobile robots equipment (e.g., arm). This approach relives at first the agent system and at second improves the overall system operation. By a flexible generic design we achieve that our implementation can handle different arm configurations and abstract it in form of a common interface for the upper level agent.

Publication: 2012 19th International Conference on Mechatronics and Machine Vision in Practice (M2VIP)

Year: 2012

ISSN:

ISBN: 978-0-473-20485-3

DOI:

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6484578

Publisher: IEEE

## Automated code generation for programmable logic controllers based on knowledge acquisition from engineering artifacts: Concept and case study

Authors: Michael Steinegger; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: The effort for design and implementation of process automation systems increases with the complexity of modern production plants. To shorten the implementation phase we propose a conceptual approach for automated code generation for programmable logic controllers (PLCs) based on knowledge acquisition from standardized engineering artifacts and their corresponding tool database. Ontologies are defined for each engineering domain artifact, representing the concepts and relations specified in the associated domain standards. An automated data extraction and population of the domain-specific ontologies together with semi-automated mapping definitions between common engineering objects then enables a rule-based code generator to query the ontologies. The query results are translated afterward into PLC code by applying a rule transformation algorithm.

Publication: Proceedings of 2012 IEEE 17th International Conference on Emerging Technologies & Factory Automation (ETFA 2012)

Year: 2012

ISSN: 1946-0759

ISBN: 978-1-4673-4736-5

DOI: 10.1109/ETFA.2012.6489546

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6489546

Publisher: IEEE

## Towards an increased reusability of distributed control applications modeled in IEC 61499

Authors: Ingo Hegny; Thomas Strasser; Martin Melik-Merkumians; Monika Wenger; Alois Zoitl

Author Affiliations: Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Energy Department, AIT Austrian Institute of Technology, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria

Keywords:

Abstract: Reusability of control code is crucial for future industrial automation in order to allow the development of high quality control systems in less time and with less cost. A key stopper for automation software reuse is the current intertwining of control logic with hardware specific code. Existing approaches that tackled such a problem could lead to improvements but will not sufficiently solve this issue. In this work we investigate a concept based on a logical grouping of I/Os to so called Instrumentation- and Control-Points and decoupling them from the control application by applying IEC 61499's adapter concept. In two industrial motivated application examples we show that this concept fulfills the requirements for increasing the reusability of control code by separating control logic from hardware specific code. Moreover, it leads to a better application software structure which is easier to maintain and to understand.

Publication: Proceedings of 2012 IEEE 17th International Conference on Emerging Technologies & Factory Automation (ETFA 2012)

Year: 2012

ISSN: 1946-0759

ISBN: 978-1-4673-4736-5

DOI: 10.1109/ETFA.2012.6489639

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6489639

Publisher: IEEE

## Towards OPC UA as portable SOA middleware between control software and external added value applications

Authors: Martin Melik-Merkumians; Thomas Baier; Michael Steinegger; Wilfried Lepuschitz; Ingo Hegny; Alois Zoitl

Author Affiliations: Vienna University of Technology, Automation and Control Institute, Vienna, Austria; MicroSys Electronics GmbH, Germany; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria

Keywords:

Abstract: Automation systems (ASs) based on Service-Oriented Architecture (SOA) are becoming more wide-spread. Due to their inherent property of separating the hardware-specific implementation from the logical work- or control-flow, SOA-based application programming is regarded as the next logical step in AS programming. Several successful attempts for implementing SOA-based AS have been made, but always with non-industrial, non-standard software like Devices Profile for Web Services. Based on the requirements of typical industrial SOA-based AS application, we will show that the industry standard data acquisition software OPC Unified Architecture is capable to serve as a SOA-based middleware.

Publication: Proceedings of 2012 IEEE 17th International Conference on Emerging Technologies & Factory Automation (ETFA 2012)

Year: 2012

ISSN: 1946-0759

ISBN: 978-1-4673-4736-5

DOI: 10.1109/ETFA.2012.6489640

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6489640

Publisher: IEEE

## Implementation guidelines for closed loop control algorithms on PLCs

Authors: Reinhard Hametner; Georg Schitter; Andreas Voigt; Alois Zoitl

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; VOIGTWIPP Engineers GmbH, Vienna, Austria; Fortiss GmbH, Munchen, Germany

Keywords: Automatic control systems development; Industrial automation systems; IEC 61499; IEC standards; Process control; Actuators; Delay effects; Delays; Mathematical model

Abstract: The integration of closed loop control algorithms into industrial control systems represents an important topic in the automation domain. Timing constraints have to be taken into account, often leading to a compromise between real-time capabilities of the control and accuracy of the calculated values. Due to its event-based execution model, IEC 61499 bears advantages concerning the closed loop control application implementation. This provides flexibility and allows the implementation of various and more sophisticated feedback algorithms. The work described in this paper is concerned with these different implementation aspects. A detailed analysis is presented concerning their timing characteristics and solutions are proposed for the actual realization of these design variants by applying IEC 61499 function blocks.

Publication: 2013 IEEE International Conference on Industrial Technology (ICIT)

Year: 2013

ISSN:

ISBN: 978-1-4673-4568-2

DOI: 10.1109/ICIT.2013.6505860

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6505860

Publisher: IEEE

## Developing modular reusable IEC 61499 control applications with 4DIAC

Authors: Alois Zoitl; Thomas Strasser; Gerhard Ebenhofer

Author Affiliations: Fortiss GmbH, Munich, Germany; Austrian Institute of Technology, Vienna, Austria; PROFACTOR GmbH, Steyr, Austria

Keywords:

Abstract: A higher flexibility and adaptability in industrial automation systems is an important requirement which has to be addressed in industrial systems today. New software architectures for the corresponding control environments allowing to develop modular and reusable code, are necessary. The IEC 61499 standard was especially developed for distributed industrial automation systems addressing such needs but its realization and the provision of corresponding software tools can be cost intensive. Using open source developments can provide helpful benefits. This paper therefore investigates the usage of the IEC 61499 compliant open source environment 4DIAC for developing modular and reusable control code. Moreover, future improvements are identified in order to enhance its usability for industrial automation applications.

Publication: 2013 11th IEEE International Conference on Industrial Informatics (INDIN)

Year: 2013

ISSN: 2378-363X

ISBN: 978-1-4799-0752-6

DOI: 10.1109/INDIN.2013.6622910

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6622910

Publisher: IEEE

## System requirements in industrial automation

Authors: Carlos C. Insaurralde; Alois Zoitl

Author Affiliations: Institute of Sensors, Signals and Systems, Heriot-Watt University, Edinburgh, UK; Fortiss GmbH, Technical University of Munich, Munich, Germany

Keywords: software analysis and design; factory automation; requirements engineering; industrial control applications; Unified modeling language; Software; Object oriented modeling; Computational modeling; Automation; Hardware; Computer architecture

Abstract: Current engineering tools for control software development of Industrial Automation Systems (IASs) are no longer capable of dealing with the architectural demands they entail. Increasingly-complex control software architectures make developers look for more efficient modeling methodologies to deal with such complexity. This paper discusses modeling gaps by focusing on the requirements analysis and architectural/detailed design stages of the IASs. It argues for having a good requirements notation on models to order to lead developers to end up in right control software for IASs. Following this hypothesis, the objective of this paper is to review existing modeling methodologies and technologies for control software architectures from factory automation and high-integrity systems. Thus, weaknesses and strengths can be identified in the industrial automation domain but also modeling capabilities from other domains can be added. This paper reveals modeling gaps given by what current approaches can provide and what is needed. It also discusses a mitigation way to close the above gap.

Publication: 2013 11th IEEE International Conference on Industrial Informatics (INDIN)

Year: 2013

ISSN: 2378-363X

ISBN: 978-1-4799-0752-6

DOI: 10.1109/INDIN.2013.6622947

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6622947

Publisher: IEEE

## Verification of hierarchical IEC 61499 component systems with behavioral event contracts

Authors: Herbert Prähofer; Alois Zoitl

Author Affiliations: Institute for System Software, Johannes Kepler University of Linz, Linz, Austria; Fortiss GmbH, Munich, Germany

Keywords: Hierarchical automation solutions; component-based design; interface-based design; hierarchical verification; Automata; Contracts; IEC standards; Sensors; Buildings; Adaptation models; Software

Abstract: Behavioral event contracts constrain the ordering of input events received and possible output events returned from a software component. Interface automata as introduced by de Alfaro and Henzinger are a light-weight formalism that allow capturing such temporal aspects of software component interfaces and the associated theory allows answering such fundamental questions as interface compatibility, component composition, and refinement. The work presented in this paper applies the results from the theory of interface automata in a hierarchical design and verification approach for IEC 61499 automation solutions. IEC 61499 adapters and service sequences are used for specification of rich behavioral component interfaces. In this approach, components are built hierarchically in master-slave arrangements where each component defines a provided interface contract for its upper-level and specifies required interface contracts for its subcomponents. Verification methods allows verifying if a component uses all its subcomponents according to their contracts, allows checking if a concrete component satisfies a given contract, and allows computing an abstraction of a component representing its externally visible behavior.

Publication: 2013 11th IEEE International Conference on Industrial Informatics (INDIN)

Year: 2013

ISSN: 2378-363X

ISBN: 978-1-4799-0752-6

DOI: 10.1109/INDIN.2013.6622948

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6622948

Publisher: IEEE

## Developing a monitoring infrastructure for IEC 61499 devices

Authors: Alois Zoitl; Gerhard Ebenhofer; Michael Hofmann

Author Affiliations: Fortiss GmbH, Munich, Germany; PROFACTOR GmbH, Steyr, Austria; PROFACTOR GmbH, Steyr, Austria

Keywords:

Abstract: In order to cope with the upcoming demands for flexible adaptive production system a new architecture for industrial automation systems has been introduced called IEC 61499. Up to now no monitoring and debugging infrastructure has been defined for IEC 61499 although, this is a key feature for industrial automation systems as break downs and unexpected standstills needs to be solved immediately. To improve this situation this work evaluates whether existing IEC 61499 means can be used for monitoring and debugging. As existing means are either not powerful enough or not suitable for small embedded control devices a new monitoring and debugging approach is developed. The developed infrastructure has been implemented as part of the 4DIAC open source framework. Testing the new monitoring and infrastructure showed that it is capable of fulfilling the requirements and that it greatly improves distributed control system development.

Publication: 2013 IEEE 18th Conference on Emerging Technologies & Factory Automation (ETFA)

Year: 2013

ISSN: 1946-0759

ISBN: 978-1-4799-0862-2

DOI: 10.1109/ETFA.2013.6647968

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6647968

Publisher: IEEE

## Control software development in Industrial Automation

Authors: Carlos C. Insaurralde; Alois Zoitl

Author Affiliations: Institute of Sensors Signals and Systems, Heriot-Watt University, Edinburgh, UK; Fortiss GmbH, Technical University of Munich, Munich, Germany

Keywords:

Abstract: Classical programming approaches are no longer enough to implement and integrate evolved control software for Industrial Automation Systems (IASs). The multidisciplinary implementation of increasingly-sophisticated IAS capabilities makes developers look for more effective methodologies to efficiently design, build, and evaluate such software. This paper identifies gaps in the development process of IASs. Filling these gaps can help improving the coding of IAS control applications by overcoming current development limitations. This paper argues for a requirements-driven development process and an interactive integration framework to mitigate drawbacks set by engineering tools. It shows gaps given by what current tools can provide and what is needed.

Publication: 2013 IEEE 18th Conference on Emerging Technologies & Factory Automation (ETFA)

Year: 2013

ISSN: 1946-0759

ISBN: 978-1-4799-0862-2

DOI: 10.1109/ETFA.2013.6648078

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6648078

Publisher: IEEE

## Design patterns for separating fault handling from control code in discrete manufacturing systems

Authors: Michael Steinegger; Alois Zoitl; Martin Fein; Georg Schitter

Author Affiliations: Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Fortiss GmbH, Munich, Germany; Automation and Control Institute, Vienna University of Technology, Vienna, Austria; Automation and Control Institute, Vienna University of Technology, Vienna, Austria

Keywords:

Abstract: The objective of this paper is to propose a methodology for strictly separating fault detection and fault handling methods from control code in discrete manufacturing systems. In order to enable the separation, two different design patterns are elaborated. Based on an analysis of typical faults in manufacturing systems, a library of reusable function blocks for fault detection, handling, and also fault recovery is developed. These function blocks are implemented according to the international standard IEC 61499 and are applied within the design patterns. The design patterns are evaluated with the sequential control of an injection molding machine. It is shown, that the design patterns simplify the engineering and the separation of the fault detection and fault handling from control code significantly, since they provide clear design rules. Applying the proposed design patterns reduces the complexity of industrial control applications drastically. Furthermore, the function block library provides reusable and proven fault detection and fault handling methods.

Publication: IECON 2013 - 39th Annual Conference of the IEEE Industrial Electronics Society

Year: 2013

ISSN: 1553-572X

ISBN: 978-1-4799-0224-8

DOI: 10.1109/IECON.2013.6699838

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6699838

Publisher: IEEE

## A unit-test framework for event-driven control components modeled in IEC 61499

Authors: Reinhard Hametner; Ingo Hegny; Alois Zoitl

Author Affiliations: Thales Austria GmbH, Vienna, Austria; Vienna University of Technology, Automation and Control Institute, Vienna, Austria; fortiss GmbH, Munich, Germany

Keywords: Industrial control systems; automation systems; test process for automation software; unit testing; IEC 61499; IEC standards; Testing; Unified modeling language; Software; Automation; Mathematical model; Software engineering

Abstract: To cope with the need for flexibility of industrial applications, and other customer related requirements, functional control behavior is shifted from hardware to software. This leads to higher software complexity. Therefore, testing of industrial software is a key technique to ensure overall system quality. Based on an analysis of testing approaches in software engineering and requirements in industrial automation system design with IEC 61499 function blocks a new unit testing process is proposed. The implementation of a platform independent test framework for IEC 61499 function blocks shows the applicability of the proposed testing process with representative examples. The presented solution is the first test framework based on the test first development approach to increase the software quality for industrial automation systems.

Publication: Proceedings of the 2014 IEEE Emerging Technology and Factory Automation (ETFA)

Year: 2014

ISSN: 1946-0759

ISBN: 978-1-4799-4845-1

DOI: 10.1109/ETFA.2014.7005209

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7005209

Publisher: IEEE

## Capability-based planning and scheduling for adaptable manufacturing systems

Authors: Nadine Keddis; Gerd Kainz; Alois Zoitl

Author Affiliations: fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany

Keywords:

Abstract: Manufacturing enterprises can only stay profitable if they manage to flexibly respond to changes in markets by adapting their products, product variants, and product volumes. To support such variety in products, we suggest a capability-based approach for production planning and scheduling. Production plans and machines are described in terms of required capabilities and provided capabilities respectively. Additionally, the topology of the factory is described. We propose to combine these descriptions to automatically generate production schedules that consider the material flow in the factory. For each production plan, our approach generates a valid schedule for the currently available machines in the factory without manually reconfiguring the software. The evaluation of the approach on an industrial production system used for educational purposes shows the suitability of this approach.

Publication: Proceedings of the 2014 IEEE Emerging Technology and Factory Automation (ETFA)

Year: 2014

ISSN: 1946-0759

ISBN: 978-1-4799-4845-1

DOI: 10.1109/ETFA.2014.7005213

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7005213

Publisher: IEEE

## Increasing the adaptability of manufacturing systems by using data-centric communication

Authors: Nadine Keddis; Jonathan Burdalo; Gerd Kainz; Alois Zoitl

Author Affiliations: fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany

Keywords:

Abstract: Future manufacturing systems have to be more adaptable to be able to compete in fast changing markets and address specific customer demands. To increase adaptability of production systems, the software and communication infrastructures have to be adaptable as well. Current communication paradigms tightly couple manufacturing systems to communication infrastructures. Changes in the manufacturing system require manual reconfiguration of software and communication infrastructure. In this paper we define the requirements for future adaptable manufacturing systems. They have to be loosely coupled, dynamic, adaptable, and capable of plug & play. We also propose a data-centric approach to make communication systems more adaptable. Using a simplified industrial setup, we show that the approach is feasible for manufacturing systems and increases the adaptability.

Publication: Proceedings of the 2014 IEEE Emerging Technology and Factory Automation (ETFA)

Year: 2014

ISSN: 1946-0759

ISBN: 978-1-4799-4845-1

DOI: 10.1109/ETFA.2014.7005214

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7005214

Publisher: IEEE

## Towards flexible and adaptive productions systems based on virtual cloud-based control

Authors: Christian Prehofer; Alois Zoitl

Author Affiliations: Fortiss GmbH, An-Institute Technical University Munich, Munich, Germany; Fortiss GmbH, An-Institute Technical University Munich, Munich, Germany

Keywords: adaptive production; central management; thin control clients; cloud control; Production systems; Automation; Manufacturing; Supervisory control; Adaptive systems; Performance evaluation

Abstract: In order to cope with changing markets and reduced product life-cycles production systems need to get more adaptive and allow to easily introduce new products and product variants. Current solutions require that all control equipment need to be modified in such cases. In this work we propose a different approach with a strong separation of basic control of production resources from product specific behavior. The product specific behavior is managed by a central control entity which sends parts of the execution tree required for a certain to thin controllers managing the production resources. With this approach we can on one hand achieve the needed flexibility and at the other hand side achieve the timing requirements of production.

Publication: Proceedings of the 2014 IEEE Emerging Technology and Factory Automation (ETFA)

Year: 2014

ISSN: 1946-0759

ISBN: 978-1-4799-4845-1

DOI: 10.1109/ETFA.2014.7005330

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7005330

Publisher: IEEE

## Modeling production workflows in a mass customization era

Authors: Nadine Keddis; Gerd Kainz; Alois Zoitl; Alois Knoll

Author Affiliations: fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; Tech. Univ., Muenchen TUM, Garching, Germany

Keywords:

Abstract: Future manufacturing systems are required to be adaptable and react quickly on changes in markets and demands. Additionally, they should be able to support individualized products that are tailored to customer needs. Flexibility can be increased through decoupling product descriptions from manufacturing systems. Production processes are no longer described based on available resources. Instead, a generic description with all required parameters is defined once and later used with different factory setups. We propose a list of parameters and information that should be included in such a generic product description. Afterwards, we define possible structures for product descriptions that can typically occur in manufacturing systems. We evaluate the approach on an experimental setup used for educational purposes.

Publication: 2015 IEEE International Conference on Industrial Technology (ICIT)

Year: 2015

ISSN:

ISBN: 978-1-4799-7800-7

DOI: 10.1109/ICIT.2015.7125374

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7125374

Publisher: IEEE

## Behavioral type-based monitoring for IEC 61499

Authors: Monika Wenger; Alois Zoitl; Jan Olaf Blech

Author Affiliations: Fortiss GmbH, An-Institut der Technischen Universität München, München, Deutschland; Fortiss GmbH, An-Institut der Technischen Universität München, München, Deutschland; AICAUSE/RMIT University, Melbourne, Australia

Keywords:

Abstract: We present work on extending IEC 61499 with behavioral types-based specifications. Identifying components and establishing interface specifications is already a key concept of IEC 61499. Components and their interfaces are a well established concept facilitating the development, maintenance, and refactoring of software systems. Behavioral types further extend the expressiveness of interface specifications by adding regular expression-based, protocol-like usages of components. We motivate the concept and focus on a particular application area: runtime monitoring of behavioral specifications in components. This allows us to catch deviations from specified behavior automatically in an already deployed system. We present the integration into the 4DIAC runtime environment using an example.

Publication: 2015 IEEE 20th Conference on Emerging Technologies & Factory Automation (ETFA)

Year: 2015

ISSN: 1946-0759

ISBN: 978-1-4673-7928-1

DOI: 10.1109/ETFA.2015.7301447

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7301447

Publisher: IEEE

## Optimizing schedules for adaptable manufacturing systems

Authors: Nadine Keddis; Bilal Javed; Georgeta Igna; Alois Zoitl

Author Affiliations: Munich, Germany; Tech. Univ, Garching, Germany; Munich, Germany; fortiss GmbH, Guerickestr. 25, 80805 Munich, Germany

Keywords:

Abstract: Adaptability and changeability are becoming the key features of future manufacturing. With adaptability comes a need to dynamically and frequently change factory topologies throughout the life-cycle of manufacturing systems. These changes are necessary to respond to changes in markets that result in new products, production volumes, and product variants. In addition to flexibly switching between different setups, the resulting schedules still have to be optimal to a certain extent to stay profitable. In this paper, we extend a capability-based planning approach to generate timed automata models that are used to solve the scheduling problem. The capability-based approach automatically generates an action sequence that defines all necessary production resources and operations for a product. The action sequence is then automatically transformed into models in UPPAAL - a model-checker for timed automata - and used to generate a schedule for production orders. The result can then be executed on the different production resources. An example scenario based on an industrial production system used for educational purposes shows the suitability of this approach.

Publication: 2015 IEEE 20th Conference on Emerging Technologies & Factory Automation (ETFA)

Year: 2015

ISSN: 1946-0759

ISBN: 978-1-4673-7928-1

DOI: 10.1109/ETFA.2015.7301452

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7301452

Publisher: IEEE

## Cloud Based Monitoring of Timed Events for Industrial Automation

Authors: Monika Wenger; Alois Zoitl; Jan Olaf Blech; Ian Peake; Lasith Fernando

Author Affiliations: Fortiss GmbH An-Institut der Technischen, Universität München, München, Deutschland; Fortiss GmbH An-Institut der Technischen, Universität München, München, Deutschland; AICAUSE/RMIT University Melbourne Australia; AICAUSE/RMIT University Melbourne Australia; AICAUSE/RMIT University Melbourne Australia

Keywords:

Abstract: This paper presents ideas towards automatic monitoring of industrial automation devices by using a cloud based monitoring infrastructure. We are in particular aiming at fine grained timed properties that can be described using formal specification techniques such as behavioral types. Possible applications are in the areas of remote maintenance and servicing as well as commissioning and testing. Our work is based in the IEC 61499 standard.

Publication: 2015 IEEE 21st International Conference on Parallel and Distributed Systems (ICPADS)

Year: 2015

ISSN: 1521-9097

ISBN: 978-1-4673-8670-8

DOI: 10.1109/ICPADS.2015.111

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7384374

Publisher: IEEE

## Towards semantic self-description of industrial devices and control system interfaces

Authors: David Hästbacka; Alois Zoitl

Author Affiliations: Department of Automation Science and Engineering, Tampere University of Technology, Tampere, Finland; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: Information systems in production environments control and gather data in operations integrating multiple devices and systems with various communication interfaces. With the development of smart industrial environments, needing to connect heterogeneous components into systems communicating over the Internet, integration and interoperability challenges emerge. Self-description is regarded as the capability of devices and systems to include descriptions expressing the offered services and information exchange. Further by semantic descriptions they can provide interpretable, meaningful information how to use the service interface but also how to interpret the capabilities and data. The paper presents a Semantic Web technology based approach to harmonize access and utilization of devices and control systems in distributed and dynamic environments. For this two standards based ontologies are developed: an industrial plant model for hierarchical structure and a state model for operational information of system components. To demonstrate the architecture and developed models the approach is applied to the components of a small-scale example industrial process.

Publication: 2016 IEEE International Conference on Industrial Technology (ICIT)

Year: 2016

ISSN:

ISBN: 978-1-4673-8074-4

DOI: 10.1109/ICIT.2016.7474867

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7474867

Publisher: IEEE

## A model based engineering tool for ROS component compositioning, configuration and generation of deployment information

Authors: Monika Wenger; Waldemar Eisenmenger; Georg Neugschwandtner; Ben Schneider; Alois Zoitl

Author Affiliations: Fortiss GmbH, Deutschland, München; Fortiss GmbH, Deutschland, München; Fortiss GmbH, Deutschland, München; Fortiss GmbH, Deutschland, München; Fortiss GmbH, Deutschland, München

Keywords:

Abstract: Programming industrial robots requires experts -not only to create the robot applications, but also for changing them later due to different product requirements. Part of the reason for this is that all robot vendors provide their own robot programming language. Due to the language differences, robot applications cannot be reused for different robot types. Often, additional experts are required since one expert is trained only for a special robot type. This makes the use of robots uneconomical for small and medium sized enterprises. The ReApp project addresses this problem by providing a workbench based on ROS (Robot Operating System). A central part of this workbench is the skill and solution modeling tool, which allows the model-based design of robot applications composed of reusable components, and is described in this paper.

Publication: 2016 IEEE 21st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2016

ISSN:

ISBN: 978-1-5090-1315-9

DOI: 10.1109/ETFA.2016.7733559

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7733559

Publisher: IEEE

## A human in the loop corrective maintenance methodology using cross domain engineering data of mechatronic systems

Authors: Milan Vathoopan; Benjamin Brandenbourger; Alois Zoitl

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: Technology trends and market changes force modern manufacturing companies to employ complex, standalone mechatronic components for automating their production. The complexity of mechatronic components induces adverse effects on their corrective maintenance. Handling downtime of these components requires knowledge of system composition, effect of external and internal disturbances on the component etc. Recognizing the human efficiency in industrial maintenance, this paper introduces a human centered corrective maintenance methodology for mechatronic components leveraging the cross disciplinary engineering data of these components. A 3D simulation model of the components' cyber-physical principles derivable from its engineering data is proposed for supporting the human doing maintenance action. A software intensive system architecture and application methods substantiating the concept are advocated.

Publication: 2016 IEEE 21st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2016

ISSN:

ISBN: 978-1-5090-1315-9

DOI: 10.1109/ETFA.2016.7733603

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7733603

Publisher: IEEE

## A Comparison of Formal Verification Approaches for IEC 61499

Authors: Jan Olaf Blech; Per Lindgren; David Pereira; Valeriy Vyatkin; Alois Zoitl

Author Affiliations: RMIT University, Melbourne, Australia; Lulea University of Technology, Sweden; Polytechnic Institute of Porto, Portugal; Lulea University of Technology, Sweden; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: Engineering and computer science have come up with a variety of techniques to increase the confidence in systems, increase reliability, facilitate certification, improve reuse and maintainability, improve interoperability and portability. Among them are various techniques based on formal models to enhance testing, validation and verification. In this paper, we are concentrating on formal verification both at runtime and design time of a system. Formal verification of a system property at design time is the process of mathematically proving that the property indeed holds. At runtime, one can check the validity of the property and report deviations by monitoring the system execution. Formal verification relies on semantic models, descriptions of the system and its properties. We report on ongoing verification work and present two different approaches for formal verification of IEC 61499-based programs. We provide two examples of ongoing work to exemplify the design and the runtime verification approaches.

Publication: 2016 IEEE 21st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2016

ISSN:

ISBN: 978-1-5090-1315-9

DOI: 10.1109/ETFA.2016.7733636

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7733636

Publisher: IEEE

## Behavior modeling of automation components using cross-domain interdependencies

Authors: Benjamin Brandenbourger; Milan Vathoopan; Alois Zoitl

Author Affiliations: fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany

Keywords:

Abstract: Within the multi-disciplinary engineering process of a cyber-physical production system, the information about the plant is increasing steadily. Different departments work on separate domain-specific models and tools allowing a specialized view of the same system. However, data exchange and linking the heterogeneous information across domains is a critical issue. This paper investigates behavior modeling of automation components out of interdependencies coming from different disciplines such as mechanics, electrics, and software engineering. By this, the interlinking of the domain-specific models, as an enabling step towards early cross-domain validation and facilitated system evolution, allows a common understanding of the correct functionality of the system. The concept will be explained through the example of a pneumatic stopper and evaluated in AutomationML, an emerging standard in automation, to store and exchange artifacts between domain-specific engineering tools.

Publication: 2016 IEEE 21st International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2016

ISSN:

ISBN: 978-1-5090-1315-9

DOI: 10.1109/ETFA.2016.7733664

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7733664

Publisher: IEEE

## Remote monitoring infrastructure for IEC 61499 based control software

Authors: Monika Wenger; Alois Zoitl; Jan Olaf Blech; Ian Peake

Author Affiliations: Fortiss GmbH, An-Institut der Technischen Universität München, München, Deutschland; Fortiss GmbH, An-Institut der Technischen Universität München, München, Deutschland; AICAUSE/RMIT University, Melbourne, Australia; AICAUSE/RMIT University, Melbourne, Australia

Keywords:

Abstract: In this paper, we present our work on monitoring of control software behavior for PLCs. In particular, we are looking at IEC 61499-based software specifications. Monitoring is done remotely, i.e., the interface behavior of function blocks is streamed to a cloud-based service. Specifications are realized using formal languages such as 1) regular expressions, 2) timed automata, 3) temporal logic. Monitors can be automatically generated from these languages. Using our specifications, we are able to detect abnormal behavior in control software such as timing changes that can, e.g., show the presence of memory leaks or a virus. We demonstrate our ideas using an example.

Publication: 2016 8th International Congress on Ultra Modern Telecommunications and Control Systems and Workshops (ICUMT)

Year: 2016

ISSN: 2157-023X

ISBN: 978-1-4673-8819-1

DOI: 10.1109/ICUMT.2016.7765387

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7765387

Publisher: IEEE

## Handling errors in dynamic production environments

Authors: Nadine Keddis; Gerd Kainz; Benjamin Brandenbourger; Milan Vathoopan; Alois Zoitl

Author Affiliations: Fortiss GMBH, Munich, Germany; Fortiss GMBH, Munich, Germany; Fortiss GMBH, Munich, Germany; Fortiss GMBH, Munich, Germany; Fortiss GMBH, Munich, Germany

Keywords:

Abstract: For future manufacturing systems with a high variety in products and a dynamic production environment, concepts for adapting production are becoming more important. Errors in processes need to be detected quickly and a fast reaction is necessary to prevent failures. Minimizing production stops and swiftly getting back to production is one main goal. Manufacturing systems have to become more intelligent to be able to autonomously react on errors. We propose an approach for explicitly modeling error handling steps in production workflows and using these models to influence the production process. Depending on the type of error, different strategies for resolving the error are executed. The error handling is embedded into an autonomous planning architecture for adaptable manufacturing systems. The approach is evaluated using an experimental setup that is designed for educational purposes. The results are presented and discussed in this paper.

Publication: 2016 IEEE 14th International Conference on Industrial Informatics (INDIN)

Year: 2016

ISSN: 2378-363X

ISBN: 978-1-5090-2871-9

DOI: 10.1109/INDIN.2016.7819149

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7819149

Publisher: IEEE

## Engineering of automation systems using a metamodel implemented in AutomationML

Authors: Benjamin Brandenbourger; Milan Vathoopan; Alois Zoitl

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: The commission and adaptation of modern automation systems is cost-intensive, error-prone and requires expertise. A large part is attributed to the engineering and programming process of manufacturer-specific components. Unifying the way of describing and controlling hardware results in a higher flexibility of the utilized hardware. This paper introduces a metamodel which allows a more efficient and flexible engineering of industrial automation systems throughout the system life cycle. The resulting model-based engineering approach utilizes highly abstracted models of automation components stored in the metamodel to form more specific models. By applying inheritance and classes, paradigms of object-oriented programming are followed to ensure better re-usability and interchangeability of modeled components. For evaluating the proposed concept the corresponding engineering data model is implemented in AutomationML.

Publication: 2016 IEEE 14th International Conference on Industrial Informatics (INDIN)

Year: 2016

ISSN: 2378-363X

ISBN: 978-1-5090-2871-9

DOI: 10.1109/INDIN.2016.7819187

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7819187

Publisher: IEEE

## Generating metamodel-based descriptions of automation components in AutomationML

Authors: Benjamin Brandenbourger; Milan Vathoopan; Alois Zoitl

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: The variability of modern automation systems is getting the key factor in determining the efficiency in manufacturing. The modularity of the employed automation components contributes significantly to the level of variability by enabling multiple compositions of automation components. In order to enable a high modularity, each automation component should be modeled as an integrated mechatronic model containing information from different disciplines. This paper describes a recursive concept allowing the structured generation of manufacturer-specific models of automation components. The concept is based on a metamodel in AutomationML and implemented in a prototypical tool for evaluation purposes.

Publication: 2017 IEEE International Conference on Industrial Technology (ICIT)

Year: 2017

ISSN:

ISBN: 978-1-5090-5321-6

DOI: 10.1109/ICIT.2017.7915526

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7915526

Publisher: IEEE

## Towards an integrated plant engineering process using a data conversion tool for AutomationML

Authors: Milan Vathoopan; Benjamin Brandenbourger; Amil George; Alois Zoitl

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Technical University of Munich, Garching, Germany; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: The development process of modern automated manufacturing plants requires a concurrent engineering process that integrates different engineering disciplines. Envisioning a concurrent development process, we propose an engineering process based on an AutomationML metamodel. The proposed metamodel contains standardized mechatronic component models, which acts as the base engineering data for the disciplines and the tools involved in the process. Since the tools operate on discipline-specific data structures, a data conversion tool is introduced which parses AutomationML mechatronic model and produces specific data interpretable by the tool employed. The benefits of this approach are evaluated by generating an automation project in CODESYS Application Composer, employing the metamodel and data conversion tool with the proposed engineering process.

Publication: 2017 IEEE International Conference on Industrial Technology (ICIT)

Year: 2017

ISSN:

ISBN: 978-1-5090-5321-6

DOI: 10.1109/ICIT.2017.7915534

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7915534

Publisher: IEEE

## Modeling and verifying behavioral constraints for automation systems

Authors: Benjamin Brandenbourger; Milan Vathoopan; Alois Zoitl

Author Affiliations: CAX-Service GmbH, Weichs, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany

Keywords:

Abstract: A technical plant behavior using a functional description forms the basis for common understanding of different disciplines and is used for the draft of hardware and software. Correlations between specific functions of the automation components and system can be allowed or denied in the behavior model describing the tended reaction. This contribution proposes an approach for modeling and verifying formal behavioral constraints of automation systems. The approach is realized either with finite state machines or with regular expressions. Furthermore, this work presents a methodology to convert verbalized constraints into finite state machines or regular expressions. The approach is evaluated by means of a pick & place unit.

Publication: 2017 IEEE 15th International Conference on Industrial Informatics (INDIN)

Year: 2017

ISSN: 2378-363X

ISBN: 978-1-5386-0838-8

DOI: 10.1109/INDIN.2017.8104796

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8104796

Publisher: IEEE

## Device adapter concept towards enabling plug&produce production environments

Authors: Kirill Dorofeev; Chih-Hong Cheng; Magno Guedes; Pedro Ferreira; Stefan Profanter; Alois Zoitl

Author Affiliations: Fortiss GmbH, An-Institut Technische Universitat Miinchen, Munich, Germany; Fortiss GmbH, An-Institut Technische Universität München, Munich, Germany; Wolfson School of Mechanical and Manufacturing Engineering Loughborough University, Loughborough, United Kingdom; Introsys - Integration for Robotics Systems SA, R&D Department, Quinta do Anjo, Portugal; Fortiss GmbH, An-Institut Technische Universität München, Munich, Germany; Fortiss GmbH, An-Institut Technische Universität München, Munich, Germany

Keywords:

Abstract: Modern manufacturing systems require a transformation from mass production towards mass customization. This results in a trend towards more agile production lines. It also demands a reduction of configuration times when building the production line as well as faster reconfiguration when adding new hardware and product variants to the manufacturing line. This paper introduces the concept of a device adapter that allows the device to be seamlessly plugged into the agile production systems. The device adapter wraps the device functionality and offers it as a service, hiding away the low-level process capability (skill) implementation and allowing to formally represent the production steps. Preliminary tests have been performed on an industrial demonstrator that simulates a real manufacturing process.

Publication: 2017 22nd IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2017

ISSN: 1946-0759

ISBN: 978-1-5090-6506-6

DOI: 10.1109/ETFA.2017.8247570

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8247570

Publisher: IEEE

## Increasing control application reusability through generic device configuration model

Authors: Waldemar Eisenmenger; Johannes Meßmer; Monika Wenger; Alois Zoitl

Author Affiliations: Industrie 4.0 fortiss GmbH, Deutschland, Munchen; Industrie 4.0, fortiss GmbH, Deutschland, München; Industrie 4.0 fortiss GmbH, Deutschland, Munchen; Industrie 4.0 fortiss GmbH, Deutschland, Munchen

Keywords:

Abstract: Nowadays it is desirable to operate flexible production plants, where products can be produced in various individual designs. As a result, more functionality needs to be integrated into existing control systems, which rapidly increases the complexity of the control applications and brings the programmable logic controllers to their limits. Unfortunately, control applications are hardly reusable for other platforms. Increasing the reusability of control applications is, therefore, an important task, which can be achieved by a strict separation of control logic and hardware configuration. Current standards lack this separation, as there is usually hardware dependent software on the application level. This paper introduces a generic device configuration model, applicable to common standards in the industrial automation domain. With this model, it is shown how to control applications can specify generic I/O requirements which are then linked to the specific I/Os during the final deployment of the specific control devices.

Publication: 2017 22nd IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2017

ISSN: 1946-0759

ISBN: 978-1-5090-6506-6

DOI: 10.1109/ETFA.2017.8247577

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8247577

Publisher: IEEE

## Towards an industry 4.0 compliant control software architecture using IEC 61499 & OPC UA

Authors: Tarik Terzimehic; Monika Wenger; Alois Zoitl; Andreas Bayha; Klaus Becker; Thorsten Müller; Hubertus Schauerte

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; SMS group GmbH, Hilchenbach; SMS group GmbH, Hilchenbach

Keywords:

Abstract: The fourth industrial revolution introduced additional requirements on the industrial systems' control software in order to cope with current manufacturing systems' flexibility demands. These requirements include, among others, a dynamic reconfigurability, software reusability and an external service orchestration. This work presents the design of an industry 4.0 compliant control software architecture resulting from an iterative design process. The architecture is based on the reconfiguration services of the IEC 61499 standard and the service orchestration via OPC UA. We demonstrate the software architecture's compliance to the industry 4.0 requirements on an aluminum cold rolling mill plant demonstrator.

Publication: 2017 22nd IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2017

ISSN: 1946-0759

ISBN: 978-1-5090-6506-6

DOI: 10.1109/ETFA.2017.8247718

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8247718

Publisher: IEEE

## Interoperability and Integration in Future Production Systems

Authors: Christian Huemer; Gerti Kappel; Manuel Wimmer; Henderik A. Proper; Siegfried Reich; Wernher Behrendt; Stefan Thalmann; Georg Weichhart; Alois Zoitl

Author Affiliations: Business Informatics Group, TU Vienna & Centre of Digital Production (CDP), Vienna, Austria; Business Informatics Group, TU Vienna & Centre of Digital Production (CDP), Vienna, Austria; Business Informatics Group, TU Vienna & Centre of Digital Production (CDP), Vienna, Austria; Luxembourg Institute of Science and Technology, Luxembourg, Luxembourg; Salzburg Research, Salzburg, Austria; Salzburg Research, Salzburg, Austria; Institute for Interactive Systems and Data Science, Graz University of Technology & Pro Future Graz, Graz, Austria; Flexible Production Systems, Pro2 Future, Steyrgleink, Austria; LIT Cyber-Physical Systems for Engineering and Production Lab, Johannes Kepler University, Linz, Austria

Keywords: Enterprise Application Integration; Enterprise Modeling; Business Process Modeling; Enterprise Integration; Enterprise Interoperability; Model-driven Control; Interoperability; Business; Production systems; Standards; Ontologies; Informatics

Abstract: This panel discussion in the context of the IEEE International Conference of Business Informatics (CBI2018) focuses on topics that allow systems to interact and exchange information. Every system in this context has its own world model. Interactions between two systems will involve a partially shared model (including e.g. standard interfaces), and two detailed, private models.

Publication: 2018 IEEE 20th Conference on Business Informatics (CBI)

Year: 2018

ISSN: 2378-1971

ISBN: 978-1-5386-7017-0

DOI: 10.1109/CBI.2018.10067

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8453953

Publisher: IEEE

## Skill-based Engineering Approach using OPC UA Programs

Authors: Kirill Dorofeev; Alois Zoitl

Author Affiliations: fortiss GmbH., Guerickestr. 25, Munich, Germany; Johannes Kepler University Altenbergstr. 69, Linz, Austria

Keywords: OPC UA Programs; Skill-based Engineering; Plug-and-Produce; State Machines; IEC Standards; Service-oriented architecture; Automation; Task analysis; Control systems

Abstract: The modern manufacturing and production systems are changing into a flexible factory layout that raises a demand for distributed control systems, where various components from different vendors communicating over their capabilities (skills) to execute a production task. This paper offers a way of how the skills, offered by an automation system component, can be represented using a generic interface to allow the higher control levels to easily orchestrate the skills available in the system and control their execution in the runtime. We show how a skill can be modeled using a Finite State Machine and present a concrete example how the concept can be realized by means of the OPC UA communication protocol.

Publication: 2018 IEEE 16th International Conference on Industrial Informatics (INDIN)

Year: 2018

ISSN: 2378-363X

ISBN: 978-1-5386-4830-8

DOI: 10.1109/INDIN.2018.8471978

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8471978

Publisher: IEEE

## Connecting PLCs With Their Asset Administration Shell For Automatic Device Configuration

Authors: Monika Wenger; Alois Zoitl; Thorsten Müller

Author Affiliations: fortiss GmbH Guerickestr. 25, München; fortiss GmbH Guerickestr. 25, München; SMS group GmbH Wiesenstrasse 31, Hilchenbach

Keywords:

Abstract: Current industrial automation systems integrate structural information and component configuration data within the code of their programmable logic controllers. This prevents the demanded flexibility and adaptability of Industrie 4.0 systems. The asset administration shell provides a defined mechanism for finding, accessing and interpreting standardized and vendor specific data of an asset. Within this work the asset administration shell has been analyzed according to its structure, its location, and its implementation forms. Based on that a concept is proposed to provide event driven run-time access for components to the asset administration shell, which enables an automatic self-configuration infrastructure for component instances. The proposed concept is applied on the logistic part of an aluminium cold rolling mill, provided by the SMS group. For demonstration the structural information of the logistic components has been described in terms of an AutomationML file, which has been loaded into a BaseX Database. The database content represents the asset administration shell, which is accessed during runtime by XQuery requests.

Publication: 2018 IEEE 16th International Conference on Industrial Informatics (INDIN)

Year: 2018

ISSN: 2378-363X

ISBN: 978-1-5386-4830-8

DOI: 10.1109/INDIN.2018.8472022

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8472022

Publisher: IEEE

## AutomationML Mechatronic Models as Enabler of Automation Systems Engineering: Use-case and Evaluation

Authors: Milan Vathoopan; Hendrik Walzel; Waldemar Eisenmenger; Alois Zoitl; Benjamin Brandenbourger

Author Affiliations: Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; Fortiss GmbH, Munich, Germany; CAX-Service GmbH, Weichs, Germany

Keywords:

Abstract: The industrial automation systems are slowly changing from a centralized architecture to a modularized, system of systems architecture nowadays. Subsequently, there are efforts to replace the classical sequential plant engineering by systems engineering, where the distributed automation entities in a plant represent a system. Considering this revamp, we propose AutomationML based mechatronic models as an enabler for automation systems engineering. Aggregating requirements from a motivating example, a prototypical implementation of a mechatronic model in AutomationML and its potentials concerning automation systems engineering are presented. A use case and its evaluation is detailed where these mechatronic models are visualized for model-based automation engineering or re-engineering. Initial results and future directions are presented.

Publication: 2018 IEEE 23rd International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2018

ISSN: 1946-0740

ISBN: 978-1-5386-7109-2

DOI: 10.1109/ETFA.2018.8502623

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8502623

Publisher: IEEE

## Enable Co-Simulation for Industrial Automation by an FMU Exporter for IEC 61499 Models

Authors: Jose Cabral; Monika Wenger; Alois Zoitl

Author Affiliations: Fortiss Gmbh, Forschungs institut des Freistaats Bayern für softwareintensive Systeme und Services, München, Deutschland; Fortiss Gmbh, Forschungs institut des Freistaats Bayern für softwareintensive Systeme und Services, München, Deutschland; Fortiss Gmbh, Forschungs institut des Freistaats Bayern für softwareintensive Systeme und Services, München, Deutschland

Keywords:

Abstract: Different causes have contributed to the shift of paradigm in the automation field from centralized to modular and distributable. Software and hardware of Programmable Logic Controllers (PLCs) have evolved to be synchronized with the demands nowadays and new standards are trying to follow this trend. One of them is the IEC 61499 standard, which is intended for modelling distributed industrial solutions with a vendor-independent format. This shifting is also bringing new challenges and this paper focuses on the virtual commissioning of plants, which can become a harder task when the system is distributed and involves different interconnected modules. A major problem when doing a virtual commissioning is the coupling between the different physical systems and controlling tools since many vendors still offer closed integrated solutions. Functional Mockup Interface (FMI) is a standard for a cosimulation interface which intends to fill the gaps between different modelling tools, by packaging the models into Functional Mockup Unit (FMU) and allowing a co-simulation master algorithm to have access to the inside model through the proposed interface. This paper presents a mapping between IEC 61499 models and the FMI standard and an implementation of a tool that can export IEC 61499 models into FMUs, which would allow the co-simulation of physical plants and the PLCs software that controls it. An experiment is shown where a simple Proportional-Integral-Derivative (PID) controller of a tank system is exported as an FMU and co-simulated together with a tank system modelled using OpenModelica.

Publication: 2018 IEEE 23rd International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2018

ISSN: 1946-0740

ISBN: 978-1-5386-7109-2

DOI: 10.1109/ETFA.2018.8502654

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8502654

Publisher: IEEE

## An Approach for an Automated Adaption of KPI Ontologies by Reusing Systems Engineering Data

Authors: Hendrik Walzel; Milan Vathoopan; Alois Zoitl; Alois Knoll

Author Affiliations: fortiss GmbH, Research Institute of the Free State of Bavaria, Munich, Germany; fortiss GmbH, Research Institute of the Free State of Bavaria, Munich, Germany; LIT Cyber Physical Systems Lab, Johannes Kepler University Linz, Linz, Austria; Chair of Robotics, Technical University of Munich, Munich, Germany

Keywords: reconfigurable manufacturing systems; semantic data integration; KPI; OEE; systems engineering; Semantics; Modeling; Knowledge based systems; Ontologies; Manufacturing systems

Abstract: Technological progress leads to an increased utilization of data analysis and Business Intelligence that support manufacturing management decisions. Many promising solutions utilize semantic technologies. However, the deployment and maintenance of semantic technologies especially in reconfigurable manufacturing environments require a lot of manual effort. Concepts to embed them in an automated environment, as required by Reconfigurable Manufacturing Systems, are limited. In this paper, we present an approach to reuse systems engineering data to guide an automated process that updates a production data knowledge base. Thereby, an ontology that integrates distributed operational data to compute Key Performance Indicators such as the Overall Equipment Effectiveness index can be updated during the manufacturing reconfiguration process. This reduces the effort to handle the required changes of semantic data integration systems and enables a cost-effective adaption of the Business Intelligence for Reconfigurable Manufacturing Systems.

Publication: 2019 24th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2019

ISSN: 1946-0740

ISBN: 978-1-7281-0304-4

DOI: 10.1109/ETFA.2019.8869083

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8869083

Publisher: IEEE

## Agile Operational Behavior for the Control-Level Devices in Plug&Produce Production Environments

Authors: Kirill Dorofeev; Stefan Profanter; Jose Cabral; Pedro Ferreira; Alois Zoitl

Author Affiliations: fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; fortiss GmbH, Munich, Germany; Wolfson School of Mechanical and Manufacturing Engineering, Loughborough University, Loughborough, United Kingdom; Johannes Kepler University, Linz, Austria

Keywords: Reconfigurable Manufacturing Systems; Skill-Based Engineering; AutomationML; OPC UA; Workstations; Automation; Manufacturing systems; Software

Abstract: The ongoing manufacturing systems transformation from mass production towards mass customization requires more flexible engineering solutions than the existing ones. The recently proposed control architectures target, among other plug-and-produce features, a reduction of configuration times. This is relevant for building a new production line as well as for faster reconfiguration when adding new hardware and product variants to an existing manufacturing line. This paper identifies operational requirements for such reconfiguration scenarios and proposes a way to implement them using the concept of a device adapter. The device adapter contains a device description and constantly updates it following the reconfiguration changes happening in a manufacturing system. This allows not only to detect the changes in the hardware, which appear in the production system, using the device discovery mechanisms but also automatically adapt the software. Preliminary tests have been performed on a demonstrator that shows both virtual and physical executions combined in a single system. The proposed solution supports automatic hardware and software reconfiguration on-the-fly without a need to stop and restart the whole production system.

Publication: 2019 24th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2019

ISSN: 1946-0740

ISBN: 978-1-7281-0304-4

DOI: 10.1109/ETFA.2019.8869208

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8869208

Publisher: IEEE

## Planning and Engineering Component-Based Automation Systems in AutomationML

Authors: Milan Vathoopan; Jose Cabral; Monika Wenger; Alois Knoll; Alois Zoitl

Author Affiliations: fortiss GmbH, 80805 Munich, Germany; fortiss GmbH, 80805 Munich, Germany; fortiss GmbH, 80805 Munich, Germany; Technical University of Munich, 85748 Garching, Germany; Johannes Kepler University, 4040 Linz, Austria

Keywords:

Abstract: Foreseeing a component based automation system architecture in the future, AutomationML consortium is developing a meta-model named AMLComponentMetamodel. The AMLComponentMetamodel defines different entities for modeling mechatronic aspects of an automation component in AutomationML. However, providing a methodology for using AMLComponentMetamodel for component oriented automation system engineering is beyond the scope of the AMLComponentMetamodel. We propose a novel methodology and modeling means for planning and engineering component based automation systems in AutomationML. A tool implementation demonstrate the use case of the presented methodology and modeling means. The discussion shows that our approach brings substantial improvement to the state of the art engineering process and simplifies the component based automation system engineering.

Publication: 2019 24th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2019

ISSN: 1946-0740

ISBN: 978-1-7281-0304-4

DOI: 10.1109/ETFA.2019.8869437

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8869437

Publisher: IEEE

## Usability of Development Tools: A CASE-Study

Authors: Thomas Weber; Alois Zoitl; Heinrich Hußmann

Author Affiliations: Fortiss GmbH, Munich, Germany; Johannes Keppler University, Linz, Austria; Ludwig-Maximilans-University, Munich, Germany

Keywords: Model-Driven Engineering; CASE Tool; Usability; 4diac; Tools; Usability; Interviews; Task analysis; Computer aided software engineering; Model driven engineering; Computational modeling

Abstract: To facilitate model-driven development in practice, we need tools that support and empower developers. Many of the tools for it, however, are somewhat lacking with respect to usability, which can act as a major obstacle in adopting a model-driven approach and impede productivity. Efforts to find concrete usability flaws in model-driven tools are still relatively rare, and in the human computer interaction community, usability for highly specialized expert software is also not a prominent topic. In this work we conduct an evaluation using a number of usability evaluations methods on the 4diac IDE as an example of a model-driven engineering tool to see what works and where the problems are. With those different methods we found a considerable number of usability issues of varying severity as well as some indication which methods work in what context. These findings of course help improving the 4diac IDE specifically but also offer more general insights that may benefit other tools in improving their user experience. Overall our evaluation shows that there is a definite need for better usability and more evaluation of it.

Publication: 2019 ACM/IEEE 22nd International Conference on Model Driven Engineering Languages and Systems Companion (MODELS-C)

Year: 2019

ISSN:

ISBN: 978-1-7281-5126-7

DOI: 10.1109/MODELS-C.2019.00037

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8904489

Publisher: IEEE

## A Survey: Microservices Architecture in Advanced Manufacturing Systems

Authors: Aydin Homay; Alois Zoitl; Mário de Sousa; Martin Wollschlaeger

Author Affiliations: Faculty of Computer Science, Technische Universität Dresden, Dresden, Germany; LIT | CPS Lab, Johannes Kepler University Linz, Linz, Austria; Faculty of Enigineering, University of Porto, Porto, Portugal; Faculty of Computer Science, Technische Universität Dresden, Dresden, Germany

Keywords: Automation; Microservices; Granularity; Flexibility; Production; Function Block; Measurement; Surveys; Architecture; Semantics; Microservice architectures; Production; Fourth Industrial Revolution; Synchronization; Plugs; Manufacturing systems

Abstract: Plug & Produce is an important part of the 4th industrial revolution (I4.0) that focuses on product development and production scenarios, demanding rapid adaptation to customer needs, with minimum effort, and no business interruption. Achieving this requires the use of flexible and agile automation systems. Microservices Architecture can be an opportunity to bring such flexibility and agility to industrial automation systems. Since Microservices Architecture is a new paradigm in service-oriented systems, an in-depth analysis from the industrial automation perspective is necessary in order to figure out why and how this new architecture could be helpful to build flexible automation systems. In this paper we first clearly describe and characterize the Microservices Architecture. We next discuss an existing paradox in microservice granularity, and suggest an approach to solve the mentioned paradox. Then we compare this new approach to the Service Oriented Architecture, highlight the key (dis)advantages of utilizing Microservice Architecture in building flexible automation systems that fits in 4th industrial revolution needs, and describe the challenges to its future adoption.

Publication: 2019 IEEE 17th International Conference on Industrial Informatics (INDIN)

Year: 2019

ISSN: 1935-4576

ISBN: 978-1-7281-2928-0

DOI: 10.1109/INDIN41052.2019.8972079

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8972079

Publisher: IEEE

## Granularity Cost Analysis for Function Block as a Service

Authors: Aydin Homay; Alois Zoitl; Mário de Sousa; Martin Wollschlaeger; Christos Chrysoulas

Author Affiliations: Faculty of Computer Science, Technische Universität Dresden, Dresden, Germany; LIT | CPS Lab, Johannes Kepler University Linz, Linz, Austria; Faculty of Enigineering, University of Porto, Porto, Portugal; Faculty of Computer Science, Technische Universität Dresden, Dresden, Germany; Faculty of Engineering, London South Bank University, London, United Kingdom

Keywords: Flexible Automation; SOA; Microservices; Granularity; Architecture; Protocols; Semantics; Refining; Microservice architectures; Programming; Mathematical models; Complexity theory; Cost benefit analysis; Synchronization; Informatics

Abstract: The main challenge of exposing IEC61499 or IEC61131-3 Function Blocks as a service remains in adopting service-oriented concepts in function block programming. Implementing an IEC61499 or IEC61131-3 Function Block that is being accessed via service-oriented protocols is straight forward. The main challenge remains in modeling a Function Block as a service. Adopting service-oriented concepts like Service Oriented Architecture or Microservice Architecture requires tackling challenges like service granularity, (de)composition, etc. For instance, too coarse-grained services could lead to significant drawbacks, while too fine-grained services could increase the system’s overall complexity, introducing semantic tight coupling and bringing about communication overhead. Therefore, understanding whether a service (de)composition is adding any value could help us to identify the best service granularity. Finding the best service granularity means knowing how many Function Blocks could be exposed into one service. This could undeniable lead to improvement in resource consumption especially in constraint environments. In this paper we design a cost analysis function for calculating the overhead of service decomposition. This work will help to answer one of the most important aspects of the service-oriented approach, called service granularity in the scope of Function Block as a Service.

Publication: 2019 IEEE 17th International Conference on Industrial Informatics (INDIN)

Year: 2019

ISSN: 1935-4576

ISBN: 978-1-7281-2928-0

DOI: 10.1109/INDIN41052.2019.8972205

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8972205

Publisher: IEEE

## A Service Bus Concept for Modular and Adaptable PLC-Software

Authors: Virendra Ashiwal; Alois Zoitl; Matthias Konnerth

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; ENGEL Austria GmbH, Schwertberg, Austria

Keywords: Factory Automation; control software; middle-ware; architecture; service Bus; PLC software; software components; Production systems; Adaptive systems; Software architecture; Conferences; Programmable logic devices; Computer architecture; Software

Abstract: How flexible and adaptive a production system can be, unquestionably depends on its software architecture and the level of modularity, flexibility, and adaptability of its software components. Programmable Logic Controllers (PLCs) are responsible for the functionalities of machines in the production system. Therefore PLC-software architecture and its software components play a vital role in a flexible, modular, and adaptive production system. In the current scenario, PLC software components use global variables to interact with each other to deliver certain machine functionality. Having global variables in PLC-software, increase hidden dependencies, reduces flexibility thus results in a less modular and less adaptable production system.In this paper, we are evaluating a service bus concept for modular and adaptable PLC-software that controls modular machines and production cells. As a result, a list of requirements for realizing such a concept is proposed.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9211908

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211908

Publisher: IEEE

## Towards a Modular Architecture for Industrial HMIs

Authors: Muddasir Shakil; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: micro-services; HMI; modular production systems; Cyber-Physical System; Couplings; Production systems; Runtime; Philosophical considerations; Conferences; Data acquisition; Organizations

Abstract: This paper presents a work in progress on a modular architecture design of industrial HMIs. The proposed approach is based on a micro frontend architecture style for developing web applications. It allows developers and integration engineers to build an HMI from distributed and modular shop-floor components called micro frontend. Each micro frontend is end-to-end integrated from its data acquisition to the user interfaces. This approach introduces an agile and modular development style of an industrial HMI for a modular and adaptive production system.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212011

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212011

Publisher: IEEE

## Service Granularity in Industrial Automation and Control Systems

Authors: Aydin Homay; Mario de Sousa; Alois Zoitl; Martin Wollschlaeger

Author Affiliations: Faculty of Computer Science, Technische Universitat Dresden, Dresden, Germany; Faculty of Enigineering, University of Porto, Porto, Portugal; LIT | CPS Lab, Johannes Kepler University Linz, Linz, Austria; Faculty of Computer Science, Technische Universitat Dresden, Dresden, Germany

Keywords: service; granularity; automation; feed-forward; feed- backward; control loop; Analytical models; Systematics; Scalability; Industrial control; Conferences; Maintenance engineering; Control systems

Abstract: Applying service-oriented concepts in industrial control and automation systems requires developing new architectural concepts to make it more adaptable to this context. In the scope of service-oriented systems one of the main challenges is defining the right granularity for every service in the system. This paper presents a systematic classification of methods to decompose the services. Identifying and using the correct granularity for each service is expected to lead to higher system flexibility, scalability, and in general to improving service deployment and maintenance. To find the best granularity for a service several approaches have been proposed, some of which are based on modeling and others based on service quality analysis. The approach we propose is based on modeling.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212048

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212048

Publisher: IEEE

## Distributed implementation of Grafcets through IEC 61499

Authors: Oscar Miguel-Escrig; Julio-Ariel Romero-Pérez; Bianca Wiesmayr; Alois Zoitl

Author Affiliations: Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain; Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain; LIT Cyber-Physical Systems Lab, Johannes Kepler University Linz, Linz, Austria; LIT Cyber-Physical Systems Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 60848; GRAFCET; IEC 61499; modelling control systems; Conferences; Decentralized control; Software; IEC Standards; Standards; Manufacturing automation; Guidelines

Abstract: A Grafcet is a standardized model for describing the behavior of systems which is popular among automation engineers. As the Grafcet standard excludes implementation details, the models are typically translated to automation software. Such software was traditionally programmed in one of the languages specified in IEC 61131-3. Nowadays, automation software is increasingly modelled in IEC 61499 which facilitates designing distributed control systems. In this paper, we define a standardized translation methodology, so that automation engineers can benefit from the advantages of IEC 61499 while continuing to use Grafcet. We discuss the differences between Grafcet and IEC 61499. We translated a Grafcet model into an IEC 61499 application to illustrate the process and derive guidelines for application designers. For the core concepts of Grafcet, we present the corresponding structure in IEC 61499.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212087

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212087

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

## Requirements for a dynamic interface model of IEC 61499 Function Blocks

Authors: Bianca Wiesmayr; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; behavior modeling; service sequence; Analytical models; Software design; Conferences; Software quality; IEC Standards; Manufacturing automation; Software engineering

Abstract: Component-based software engineering has emerged as a principle of software design to facilitate reuse and improve the software quality. This principle is supported by the domain-specific language IEC 61499, where Function Blocks are fully encapsulated software components. For a Function Block definition, a static interface description and an internal implementation are required. Service sequences describe the event flow at a component interface and are an optional dynamic interface model in IEC 61499. In general, dynamic interface models are a powerful tool for various use cases, yet service sequences are rarely used in practice due to their low expressiveness. Therefore, we identify the domain-specific requirements for a comprehensive dynamic interface model and use them for our analysis of service sequences, where several issues are identified.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212107

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212107

Publisher: IEEE

## Fault Handling in Discrete Event Systems Applied to IEC 61499

Authors: Herbert A. S. Leitão; Roberto S. U. Rosso; André B. Leal; Alois Zoitl

Author Affiliations: Electrical Engineering Postgraduate Program, Santa Catarina State University, SC, Brazil; Electrical Engineering Postgraduate Program, Santa Catarina State University, SC, Brazil; Electrical Engineering Postgraduate Program, Santa Catarina State University, SC, Brazil; Johannes Kepler University, Linz, Austria

Keywords: discrete event systems; fault diagnosis; fault tolerant control; IEC 61499; industry 4.0; smart manufacturing; Fault diagnosis; Systems operation; Process control; Computer architecture; Supervisory control; Sensor systems; Discrete-event systems

Abstract: The search for making industrial systems smarter is a chalenge present in the Industry 4.0 scope. In this new industrial era, the automation processes operate in a more flexible and adaptable way, even if there is a system fault. However, depending on the level of complexity of the system operation, faut diagnosis and fault handling procedures can become difficult to evaluate and implement, especially when it is necessary to integrate them into the control system. Based on this challeging scenario, this article presents RAFAH, a reconfiguration architecture for fault handling in industrial systems. RAFAH is composed by three operational stages that autonomously compute flexible fault tolerant control strategies, combining formal methods for faults diagnosis in discrete event systems, supervisory control theory’s extensions for modelling and designing control systems, and IEC 61499 resources for developing distributable and reconfigurable applications. The proposed methodology is validated by a case study in a fluid mixing process in which it is applied to diagnose faults and provide a new control strategy.

Publication: 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2020

ISSN: 1946-0740

ISBN: 978-1-7281-8957-4

DOI: 10.1109/ETFA46521.2020.9212177

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9212177

Publisher: IEEE

## A Novel Approach for Integrating IEC 61131-3 Engineering and Execution Into IEC 61499

Authors: Peter Gsellmann; Martin Melik-Merkumians; Alois Zoitl; Georg Schitter

Author Affiliations: Automation and Control Institute, TU Wien, Vienna, Austria; Automation and Control Institute, TU Wien, Vienna, Austria; LIT Cyber Physical Systems Lab, Johannes Kepler University Linz, Linz, Austria; Automation and Control Institute, TU Wien, Vienna, Austria

Keywords: IEC 61499; IEC 61131; interoperability; IEC Standards; Task analysis; Programming; Informatics; Software; Tools; Automation

Abstract: Automation system engineering becomes more complex, due to the trend toward more flexible, reconfigurable, and modular design approaches, like Industry 4.0. For the modeling and design of the according software, two standards are present: IEC 61131-3 and IEC 61499. In order to satisfy the requirements for modern, large scale, highly distributed applications while also supporting still existing legacy systems, the demand for a combined development framework arises, where the best of breed tool can be chosen for a given automation task. Considering that, the IEC 61499 model is extended to allow the dual development and execution of IEC 61131-3 programs, and enabling easy and correct interaction between the two paradigms. In order to verify the validity of the chosen approach, an IEC 61499 development tool and a runtime environment is modified to support IEC 61131-3. A sample application is implemented, which comprises a pure IEC 61131-3 part with a 1 ms cycle time, a pure IEC 61499 part, and a part with interaction between both subparts, in order to evaluate possible interference between the runtime parts. Experimental results show that no interference is occurring, and the chosen development approach allows the seamless integration of IEC 61131-3 and IEC 61499 in one combined development framework.

Publication: IEEE Transactions on Industrial Informatics

Year: 2021

ISSN: 1941-0050

ISBN:

DOI: 10.1109/TII.2020.3033330

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9238463

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

## Integration of ISO/IEC/IEEE 21450 Transducer Electronic Datasheets into OPC UA Information Model

Authors: Muddasir Shakil; Alois Zoitl; Mahin K. Atiq; Hans Peter Bernhard

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; Silicon Austria Labs, Linz, Austria; Silicon Austria Labs, Linz, Austria

Keywords: Cyber-Physical System; Interoperability; Industrial Internet of Thing; Device Integration; Industrial Automation; Semantic Model; Transducers; Automation; ISO Standards; Semantics; Syntactics; Production facilities; Service-oriented architecture

Abstract: Interoperability is one of the important characteristics of the cyber-physical system (CPS) based automation system. Engineers connecting field devices and control applications in an automation system regularly encounter interoperability problems. ISO/IEC/IEEE 21451 is a series of standard, which provide the building blocks to enable interoperability among field devices and control applications. transducer electronic datasheets (TEDS) are provided as a standard transducer description format by ISO/IEC/IEEE 21450. This format provisions the syntactic interoperability among heterogeneous field devices. However, open platform communication unified architecture (OPCUA) is a key enabling technology to achieve semantic and network interoperability. Therefore, the aim of this paper is to provide an integration approach for ISO/IEC/IEEE 21450 TEDS and devices in the OPCUA semantic model. We propose an ISO/IEC/IEEE 21450 based device integration concept with service oriented architecture.

Publication: 2021 17th IEEE International Conference on Factory Communication Systems (WFCS)

Year: 2021

ISSN:

ISBN: 978-1-6654-2479-0

DOI: 10.1109/WFCS46889.2021.9483596

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9483596

Publisher: IEEE

## An International Case Study on Control Software Development in Large-Scale Plant Manufacturing Companies of One Industrial Sector at Different Locations

Authors: Birgit Vogel-Heuser; Eva-Maria Neumann; Alois Zoitl; Antonio M. Gutierrez Fernandez; Rick Rabiser; Hafiyyan Sayyid Fadhlillah

Author Affiliations: Department of Mechanical Engineering TUM School of Engineering and Design Core Member of MDSI and Member of MIRMI, Institute of Automation and Information Systems, Technical University of Munich, Garching, Germany; Department of Mechanical Engineering TUM School of Engineering and Design, Institute of Automation and Information Systems, Technical University of Munich, Garching, Germany; CDL VaSiCS LIT CPS Lab, Johannes Kepler University, Linz, Linz, Austria; CDL VaSiCS LIT CPS Lab, Johannes Kepler University, Linz, Linz, Austria; CDL VaSiCS LIT CPS Lab, Johannes Kepler University, Linz, Linz, Austria; CDL VaSiCS LIT CPS Lab, Johannes Kepler University, Linz, Linz, Austria

Keywords: automated Production Systems; control software development; Programmable Logic Controllers; IEC 61131-3; Industries; Industrial electronics; Production systems; Mechatronics; Law; Supply chains; Process control

Abstract: automated Production Systems (aPS) represent a special type of mechatronic system characterized by a high complexity in hardware and software, lifetimes of up to several decades, and strong coupling of the involved disciplines, i.e., mechanics, electrics/electronics, and control software. Questionnaire studies have proven to be a valuable means of identifying obstacles in industrial software development that hinder the implementation of emerging technologies in the context of Industry 4.0 and, thus, the realization of Cyber-Physical Production Systems. However, the heterogeneity of different industrial sectors in terms of, e.g., the type of production processes or legal specifications, makes it difficult to compare the maturity of control software development across companies, even within the same industry. A software maturity benchmark for companies operating in similar industries is, however, a prerequisite for assessing a company’s strengths and weaknesses and thereby applying tailored solutions to improve the software and, thus, the competitiveness. This paper describes the results of a questionnaire study in two international companies operating in the same industrial sector. Specifically, location-, company-, and industry-specific maturity characteristics are analyzed and discussed, and it is concluded that the selected questionnaire is capable of identifying deviations and similarities in software maturity, even in an international environment, given that the companies are prefiltered based on the covered supply chain step. Hence, assuming a sufficiently large number of participants per industry, it enables a questionnaire-based industry comparison in future work, which was not possible until now.

Publication: IECON 2021 – 47th Annual Conference of the IEEE Industrial Electronics Society

Year: 2021

ISSN: 1553-572X

ISBN: 978-1-6654-0256-9

DOI: 10.1109/IECON48115.2021.9589516

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9589516

Publisher: IEEE

## Assessing the Usefulness of a Visual Programming IDE for Large-Scale Automation Software

Authors: Bianca Wiesmayr; Alois Zoitl; Rick Rabiser

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Austria

Keywords: Usefulness study; Open source software; IEC 61499; Modeling tools; Model-driven engineering; Visualization; Software maintenance; Adaptation models; Automation; Tools; Programming; Software

Abstract: Industrial control applications are usually designed by domain experts instead of software engineers. These experts frequently use visual programming languages based on standards such as IEC 61131-3 and IEC 61499. The standards apply model-based engineering concepts to abstract from hardware and low-level communication. Developing industrial control software is challenging due the fact that such systems are usually one-of-a-kind systems that have to be maintained for many years. These challenges, together with the growing complexity of control software, require very usable model-based development environments for visual programming languages. However, so far only little empirical research exists on the practical usefulness of such environments, i.e., their usability and utility. In this paper, we discuss common control software maintenance tasks and tool capabilities based on existing research and show the realization of these capabilities in 4diac IDE. We first performed a walkthrough of the demonstrated capabilities using the cognitive dimensions of notations framework from the field of human-computer interaction. We then improved the tool and conducted a user study involving ten industrial automation engineers, who used 4diac IDE in a realistic control software maintenance scenario. Our findings demonstrate how the usefulness of IDEs can be successfully investigated using a multi-phase approach that includes a walkthrough and a user study. We discuss lessons learned and derive general implications with respect to large-scale applications for developers of IDEs that we deem applicable in the context of (visual) model-based engineering tools.

Publication: 2021 ACM/IEEE 24th International Conference on Model Driven Engineering Languages and Systems (MODELS)

Year: 2021

ISSN:

ISBN: 978-1-6654-3496-6

DOI: 10.1109/MODELS50736.2021.00037

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9592491

Publisher: IEEE

## Distributed Implementation of Hierarchical Grafcets through IEC 61499

Authors: Bianca Wiesmayr; Alois Zoitl; Oscar Miguel-Escrig; Julio-Ariel Romero-Pérez

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS; Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain; Department of Systems Engineering and Design, Universitat Jaume I, Castellon, Spain

Keywords: IEC 60848; GRAFCET; IEC 61499; modeling control systems; Conferences; Tools; Control systems; Software; IEC Standards; Manufacturing automation; Manufacturing systems

Abstract: The control software of manufacturing systems has to interact with the mechanical and electrical machine parts, hence, their engineering is closely interrelated. A high-level model of this system can provide an abstract view on the system's behavior and is therefore beneficial for any engineering discipline. The language GRAFCET was developed as a domain-specific tool for specifying the operation of a production system. GRAFCET models can be structured hierarchically to regulate the behavior of a subsystem with forcing orders and enclosing steps. Based on a Grafcet, control software can be implemented in the executable modeling language IEC 61499. In this paper, we describe a step-by-step approach for implementing hierarchical features of GRAFCET with IEC 61499 models. The resulting application is well-structured and thus maintainable.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613251

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613251

Publisher: IEEE

## Towards Delta-Oriented Variability Modeling for IEC 61499

Authors: Hafiyyan Sayyid Fadhlillah; Bianca Wiesmayr; Michael Oberlehner; Rick Rabiser; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: IEC 61499; Variability Modeling; Model-driven Development; Software Product Lines; Cyber-Physical Production Systems; Production systems; Systematics; Costs; Conferences; Decentralized control; Time to market; Software

Abstract: Modern production plants are complex Cyber-Physical Production Systems with an ever-increasing share of software controlling and automating their operation. The customization of these systems to the needs of their customers and their frequent evolution over a typically long life-cycle result in a plethora of variants to be managed. However, reuse still is mainly done in an opportunistic way, relying on copy-paste-modify strategies. More systematic, strategic reuse would help to reduce costs and time to market, but requires approaches that can be applied to domain-specific languages for developing distributed control software. In this paper, we propose an approach to manage variability in IEC 61499-based systems using delta-oriented variability modeling. We discuss open challenges and outline a research agenda for variability management in IEC 61499.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613293

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613293

Publisher: IEEE

## Towards Service Deployment and Composition in Industry 4.0

Authors: Tarik Terzimehić; Kirill Dorofeev; Sebastian Bergemann; Alois Zoitl; Sebastian Voss

Author Affiliations: fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University, Linz, Austria; fortiss - Research Institute of the Free State of Bavaria, Munich, Germany

Keywords: Industry 4.0; IEC 61499; deployment synthesis; service composition; code generation; model-based development; Industries; Codes; Conferences; Prototypes; Production; Complexity theory; Optimization

Abstract: The fourth industrial revolution (Industry 4.0) anticipates unplanned changes of production processes. Production changes may trigger synthesis, and preferably optimization, of architecture-level decisions, such as service deployment and composition. Performing such architecture-level decisions manually is difficult due to the ever-rising complexity of Industry 4.0 systems. In order to (semi-)automate the architecture synthesis and optimization, we propose an approach of service deployment and composition by using existing domain models. Our contribution is threefold: (1) We suggest a workflow with domain models for architecture synthesis in the industrial automation. (2) We display the formalization on a part of the workflow and provide an initial prototype of service deployment synthesis using a satisfiability modulo theories (SMT) solver. (3) We envision a way of service composition and code generation, and prototypically implemented it as conclusion of the suggested workflow. We demonstrate the practical use of the proposed approach in the Industry 4.0 scenario, i.e., flexible production of new products.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613327

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613327

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

## Messaging Interaction Patterns for a Service Bus Concept of PLC-Software

Authors: Virendra Ashiwal; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Factory Automation; Control software; Middleware; PLC service Bus; PLC software; Software components; Interaction pattern; POU; Production systems; Software architecture; Microprocessors; Conferences; Computer architecture; Organizations; Software

Abstract: The software architecture of PLC-software has a direct influence on its adaptability, modularity, and flexibility. The software component (Program organization unit, POU) is the smallest unit of PLC-software that is responsible for providing certain machine functionality in an overall production system. The way these software components interact with each other has a significant role in the overall PLC-software architecture. To address current market demands, software components need to be atomic, modular, and loosely coupled. PLC-Service bus-based architecture enables such PLC-software. We are using this architecture as a basis. In this paper, we are evaluating available messaging interaction patterns from the enterprise IT domain. Our evaluation is based on requirements defined by the PLC-Service bus architecture. Therewith, we identified a list of interaction patterns that can be used to design interactions between software components in a PLC-Service bus environment. We use a reference production cell as a running example. To evaluate our findings, we first explain what the PLC-Service bus concept would look like for our running example. Later, we used four practical process scenarios from our running example to evaluate the applicability of identified messaging integration patterns for the PLC-Service bus.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613638

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613638

Publisher: IEEE

## A Model-based Execution Framework for Interpreting Control Software

Authors: Bianca Wiesmayr; Alois Zoitl; Antonio Garmendia; Manuel Wimmer

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL-MINT, Johannes Kepler University Linz, Linz, Austria; CDL-MINT, Johannes Kepler University Linz, Linz, Austria

Keywords: Industrial automation; IEC 61499; Operational semantics; Interpreter; Model-driven engineering; Java; Runtime; Semantics; Natural languages; IEC Standards; Standards; Open source software

Abstract: Industrial standards define domain-specific languages that are frequently used for developing control software. For instance, IEC 61499 standardizes a graphical modeling language that includes a platform-independent application model. The application is composed of Function Blocks. A runtime can execute the model by implementing the semantics that is described in the standard in natural language. By defining an interpreter for IEC 61499 models, we can directly execute them without prior code generation. This enables providing feedback directly on the model level. We present an interpreter for Basic Function Blocks, which encapsulate a state-based Execution Control Chart. An existing EMF meta-model for IEC 61499 was extended with an operational semantics implemented in Java and Xtend. The test cases are defined either in Java or as an interface model. Such a model is standardized in IEC 61499 as Service Sequences. We evaluate our interpreter by executing the Basic Function Blocks that are defined in the standard and compare our results to those of the open-source runtime 4diac FORTE. As a practical use case, we show how developers can use the interpreter for unit testing self-defined Basic Function Blocks.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613716

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613716

Publisher: IEEE

## Generation of the Orchestrator Code for Skill-Based Automation Systems

Authors: Kirill Dorofeev; Sebastian Bergemann; Tarik Terzimehić; Julian Grothoff; Michael Thies; Alois Zoitl

Author Affiliations: fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; fortiss - Research Institute of the Free State of Bavaria, Munich, Germany; PLT, Chair of Process Control Engineering, RWTH Aachen University, Germany; PLT, Chair of Process Control Engineering, RWTH Aachen University, Germany; CDL VaSiCS, LIT CPS Lab, Johannes Kepler University Linz, Austria

Keywords: Industry 4.0; skills; service-oriented architecture; IEC 61499; service composition; orchestration; PLC code generation; Industries; Codes; Decentralized control; Process control; Production; Maintenance engineering; Software

Abstract: Engineering distributed control systems is a complex task, where the complexity and, thus, costs of the software development are growing rapidly. To keep the software complexity at an acceptable level and save time for development and subsequent maintenance, new solutions are sorely needed. In this paper, we investigate the advantages of using skills - universal control device interfaces - for generating complex logic in distributed control environments. By enriching a skill interface with the information about the dynamic behavior of a component under control, we compose the functionalities of individual control devices. The logic, required for such composition, is automatically derived from the interface description and the production plan, identifying the required skill sequence. The evaluation, executed using two industrial demonstrators, shows that the approach successfully handles different behavioral models and is capable of generating fault-tolerant orchestrators, including error handling scenarios. Overall, for developing a complex logic in a distributed skill-based automation system, the proposed approach shows significant savings in development time allowing to automate the skill composition task.

Publication: 2021 26th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA )

Year: 2021

ISSN:

ISBN: 978-1-7281-2990-7

DOI: 10.1109/ETFA45728.2021.9613728

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9613728

Publisher: IEEE

## Implementing a PLC-Service bus with IEC 61499

Authors: Virendra Ashiwal; Antonio M. Gutierrez; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; CDL VaSiCS, Linz, Austria; CDL VaSiCS, Linz, Austria

Keywords: PLC-Service Bus; PLC-software; Software components; Interaction pattern; POU; Middleware; Factory Automation; Control software; Couplings; Adaptation models; Conferences; Standards organizations; Organizations; Cyber-physical systems; Software

Abstract: With an increased demand for customization, a better quality of products, and available variability in machines, enforcing machine developers to rethink how PLC-software is structured and developed. It demands the PLC-software to be adaptable, flexible, and modular. Current PLC-software uses global variables for interaction between its program organization units (POUs). Global variables increase tight coupling and reduce adaptability, flexibility, and modularity. A new architectural concept, the PLC-Service bus, was suggested to address this issue. To reduce coupling, POUs and software components of the PLC communicate via a service bus. This concept leads to two problems. There are no standard models to describe these interactions clearly, and there is no implementation of the PLC-Service bus to develop PLC-software based on message interaction patterns (MIPs). This paper uses the capping station from the VDMA R+a OpcUA Demonstrator as a running example. With an Event-driven process chain model (EPC), we describe the interactions between various software components of the capping station to identify MIPs. Based on these MIPs, we implement the PLC-software of the capping station with IEC 61499.

Publication: 2022 IEEE 5th International Conference on Industrial Cyber-Physical Systems (ICPS)

Year: 2022

ISSN:

ISBN: 978-1-6654-9771-8

DOI: 10.1109/ICPS51978.2022.9816929

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9816929

Publisher: IEEE

## Coupling and Decoupling in IEC 61499 and IEC 61131-3 Applications

Authors: Aydin Homay; Mário de Sousa; Alois Zoitl; Martin Wollschlaeger

Author Affiliations: Faculty of Computer Science, Technical University of Dresden, Dresden, Germany; Faculty of Engineering, University of Porto, Linz, Austria; LIT | CPS Lab, Johannes Kepler University Linz, Linz, Austria; Faculty of Computer Science, Technical University of Dresden, Dresden, Germany

Keywords: coupling; cohesion; decoupling; industrial automation; Couplings; Industries; Industrial control; Software systems; Software measurement; History; IEC Standards

Abstract: The history of the software industry has shown and proved that coupling and cohesion are a never-ending story in this industry. Quantifying the quality of software systems by measuring the strength of coupling and cohesion and considering it a rule that good software has low coupling between its parts and high cohesion within each part, is currently widely accepted. Every paradigm shift, new technology, language, etc. that didn`t consider this fact had to sooner or later leave this industry. It is, therefore, crucial to study and consider this fact in every new topic in the software industry. Surprisingly neither the IEC 61499 nor IEC 61131 communities have yet conducted a deep study to evaluate what coupling and cohesion really mean for Industrial Control and Automation Applications. We hope this paper will manage to fulfill this considerable gap, if not fully at least partially.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921472

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921472

Publisher: IEEE

## Supporting a Model-driven Development Process for Distributed Control Software

Authors: Bianca Wiesmayr; Alois Zoitl; Laurin Prenzel; Sebastian Steinhorst

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; Johannes Kepler University Linz, Linz, Austria; Technical University of Munich, Munich, Germany; Technical University of Munich, Munich, Germany

Keywords: Model-driven engineering; IEC 61499; Development process; Control software; Process control; Maintenance engineering; Systems engineering and theory; Software; Behavioral sciences; IEC Standards; Monitoring

Abstract: Established development processes for industrial control systems are static and struggle to adopt changing requirements. The interdisciplinary nature of such systems necessitates carefully designed interfaces between modules and components, as well as unambiguously defined requirements. The domain-specific modeling language IEC 61499 offers potentials to accelerate design processes and to introduce a model-driven approach, in which interface and behavior models are continuously refined and reused. We investigate these potentials and outline how to apply an extended development process in which implicit expert knowledge is preserved in behavior- and interface models that are currently not retained during the development. Based on a running example, we illustrate the refinement of scenarios along the development process and show how the retained information captures the expected behavior of the environment. We identify research questions and gaps in the elicitation, maintenance and utilization of these models, in particular in the domains of model-based testing, monitoring, and reconfiguration. An accelerated development process that integrates behavior models can help making future industrial control systems more dependable, flexible, and resilient during the whole life cycle.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921506

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921506

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

## Evaluation of Middleware Technologies for the PLC-Service Bus in IEC 61499

Authors: Virendra Ashiwal; Mainak Majumder; Alois Zoitl

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: PLC-Service Bus; Middleware; PLC Software; POUs; IEC 61499; Production systems; Computer architecture; Middleware; IEC Standards; Standards; Manufacturing automation

Abstract: To address current challenges of production systems such as increased number of product variants, batch size one, and shorter product life cycle, they need to be modular, loosely coupled, and more adaptable than ever. A PLC-Service bus architecture has been proposed to improve the modularity and adaptability of a PLC-software. The architecture enables software components of PLC-software to interact via middleware in a loosely coupled manner. Previous work identified a catalog of message integration patterns for PLC-software, and IEC 61499 was proposed to implement the architecture. The current version of the IEC 61499 standard does not fully support all message integration patterns from the catalog.Therefore, this paper first identifies suitable middleware technologies for IEC 61499 and, later, based on the requirements of the PLC-Service bus architecture, evaluates them to propose the suitable middleware technologies.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921536

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921536

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

## Impact of Modularization and Coupling on the Complexity of Industrial Control and Automation Systems

Authors: Aydin Homay; Martin Wollschlaeger; Mário de Sousa; Alois Zoitl

Author Affiliations: Faculty of Computer Science, Technical University of Dresden, Dresden, Germany; Faculty of Computer Science, Technical University of Dresden, Dresden, Germany; Faculty of Engineering, University of Porto, Porto, Portugal; LIT | CPS Lab, Johannes Kepler University Linz, Linz, Austria

Keywords: Vertical Coupling; Horizontal Coupling; Cynefin Framework; Automation; Couplings; Software design; Software architecture; Industrial control; Control systems; Software; Complexity theory

Abstract: Coupling could be an arbitrary property to Industrial Automation and Control Systems (ICAS) with a significant impact on complexity. Different software design approaches may result in coupling between software modules that either increase or decrease the overall system complexity. This paper proposes using the Cynefin Framework to guide the software design patterns used during the high-level design of software architecture, with the intent of reducing components coupling and overall system complexity.

Publication: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA)

Year: 2022

ISSN:

ISBN: 978-1-6654-9997-2

DOI: 10.1109/ETFA52439.2022.9921695

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9921695

Publisher: IEEE

## Using Modules to Manage the Content of IEC 61499 Type Libraries

Authors: Michael Oberlehner; Virendra Ashiwal; Alois Zoitl; James H. Christensen

Author Affiliations: LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; LIT CPS Lab, Johannes Kepler University Linz, Linz, Austria; Holobloc Inc, US

Keywords: IEC 61499; Module; Reusability; Library Management; Function Block; Runtime; Libraries; IEC Standards; Informatics

Abstract: This work analyzes the problems that arise in IEC 61499 development due to the fact that there are no ways of structuring type libraries. As a result of this analysis we derived requirements for integrating modules into the IEC 61499 specification. The modules that are portable among several runtime providers and vendors can be imported into IEC 61499 systems. Every module contains a set of function blocks that can be used inside the application. The proposed IEC 61499 module has its own version and namespace. It is also capable of defining dependencies on each other. Reusability from types can be increased by dividing the type library into several parts with the help of the proposed modules.

Publication: 2022 IEEE 20th International Conference on Industrial Informatics (INDIN)

Year: 2022

ISSN:

ISBN: 978-1-7281-7569-0

DOI: 10.1109/INDIN51773.2022.9976150

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9976150

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
