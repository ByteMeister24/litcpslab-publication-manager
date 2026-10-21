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
