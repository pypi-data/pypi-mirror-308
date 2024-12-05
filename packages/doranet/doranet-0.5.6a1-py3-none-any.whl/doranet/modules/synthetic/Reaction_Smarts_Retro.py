"""Reverse (retro-) synthetic operators in SMARTS form."""

import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class OperatorSmarts:
    name: str
    smarts: str
    reactants_stoi: typing.Optional[tuple[int | float, ...]] = None
    products_stoi: typing.Optional[tuple[int | float, ...]] = None
    enthalpy_correction: typing.Optional[float] = (
        None  # add a correction term for enthalpy filter
    )
    ring_issue: typing.Optional[bool] = (
        False  # if True, should check stoichiometry (including H) and connectivity (example: breaking 2 bonds and form a fragment, will have problem if the two fragments are connected by other parts. example2: cope rearrangements, C1 and C6 shouldn't connect, will have problem if they are) of reactants and products in a filter; ring issue could also cause RDkit error by breaking aromatic molecules, if a breaking group is directly on a aromatic molecule, consider use kekulize_flag as well (example Transesterification).
    )
    kekulize_flag: typing.Optional[bool] = (
        False  # if need to break aromatic bonds, use engine.op.rdkit(smarts, kekulize=True) to kekulize before running the SMARTS template matching
    )
    Retro_Not_Aromatic: typing.Optional[bool] = (
        False  # only useful in retro list. if true, the forward reaction don't apply to aromatic molecules; should check if number of aromatic rings increase to avoid producing aromatic molecules.
    )
    number_of_steps: typing.Optional[int] = (
        1  # optional for multi-step rxn operators, may be useful for enthalpy filter
    )
    allowed_elements: typing.Optional[tuple[str, ...]] = (
        "All",
    )  # can be used to specify the allowed elements in the reactants, and use a filter during expansion to filter out reactions if reactants contain other elements. For example, allowed_elements = ("C", "H") means this operator is intended only for hydrocarbons
    reaction_type: typing.Optional[str] = (
        "Catalytic"  # Catalytic for chemical reactions. the other option is Enzymatic, for bio rxn rules
    )


op_retro_smarts = (
    # Alkanes #############################################################
    # Selective Oxidation of Aliphatic Groups
    #    OperatorSmarts("Selective Oxidation of Aliphatic Groups",
    #                   "[C+0;!$(*=[O,S,N]);!$(*(-[O,S,N])-O);!$(*[O,S,N]*):1][O+0H:2]>>[*:1].[*:2]=[O]",
    #                   (1,),(1,0.5)),
    # Halogenation of Alkanes, Benzene
    #    OperatorSmarts("Halogenation of Alkanes, Benzene",
    #                   "[C,c;!$(*~O);+0:1][F,Cl,Br,I;+0:2].[F,Cl,Br,I;+0H:3]>>[*:1].[*:2][*:3]",
    #                   (1, 1),(1, 1)),
    # Halogenation of Methane, Halomethanes
    OperatorSmarts(
        "Halogenation of Methane, Halomethanes",
        "[C!$(*~[!F!Cl!Br!I])+0:1][F,Cl,Br,I;+0:2].[F,Cl,Br,I;+0H:3]>>[*:1].[*:2][*:3]",
        (1, 1),
        (1, 1),
    ),
    # Below are some typical cracking/pyrolysis reactions, use when necessary
    # Propane Cracking
    OperatorSmarts(
        "Propane Cracking",
        "[C+0H2:1]=[C+0H2:2].[C+0H4:3]>>[*:1][*:2][*:3]",
        (1, 1),
        (1,),
    ),
    # Butane Cracking
    OperatorSmarts(
        "Butane Cracking 1",
        "[C+0H3:1][C+0H:2]=[C+0H2:3].[C+0H4:4]>>[*:1][*:2][*:3][*:4]",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Butane Cracking 2",
        "[C+0H2:1]=[C+0H2:2].[C+0H3:3][C+0H3:4]>>[*:1][*:2][*:3][*:4]",
        (1, 1),
        (1,),
    ),
    # Pentane Cracking
    OperatorSmarts(
        "Pentane Cracking",
        "[C+0H3:1][C+0H2:2][C+0H:3]=[C+0H2:4].[C+0H4:5]>>[*:1][*:2][*:3][*:4][*:5]",
        (1, 1),
        (1,),
    ),
    # Catalytic Reforming
    OperatorSmarts(
        "Catalytic Reforming",
        "[C+0H2:1]1[C+0H2:2][C+0H2:3][C+0H2:4][C+0H2:5][C+0H2:6]1.[H][H]>>[*:1][*:2][*:3][*:4][*:5][*:6]",
        (1, 1),
        (1,),
    ),
    # Isomerization of Butane
    OperatorSmarts(
        "Isomerization of Butane",
        "[C+0H3:1][C+0H:2]([C+0H3:3])[C+0H3:4]>>[*:1][*:2][*:3][*:4]",
        (1,),
        (1,),
    ),
    # Alkane Dehydrogenation     these are used in the cracking process but may not suit general organic chemistry applications, use when necessary
    OperatorSmarts(
        "Alkane Dehydrogenation",
        "[C+0:1]=[C+0:2].[H][H]>>[*:1][*:2]",
        (1, 1),
        (1,),
        kekulize_flag=True,
        allowed_elements=("C", "H"),
    ),
    OperatorSmarts(
        "Alkane Dehydrogenation 2",
        "([C+0:1]=[C+0:2].[C+0:3]=[C+0:4].[C+0:5]=[C+0:6]).[H][H]>>([*:1][*:2].[*:3][*:4].[*:5][*:6])",
        (1, 3),
        (1,),
        kekulize_flag=True,
        number_of_steps=3,
        allowed_elements=("C", "H"),
    ),
    # Alkenes ##############################################################
    # Hydrogenation of Alkene
    OperatorSmarts(
        "Hydrogenation of Alkene",
        "[C+0!H0:1][C+0!H0:2]>>[*:1]=[*:2].[H][H]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Oxidative Cleavage of Alkenes
    OperatorSmarts(
        "Oxidative Cleavage of Alkenes",
        "[C;!$(*(=O)=O);+0:1]=[O+0:4].[C;!$(*(=O)=O);+0:2]=[O+0:5]>>[*:1]=[*:2].[*:4]=[*:5]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Oxidative Cleavage of Alkenes, Intramolecular",
        "([C;!$(*(=O)=O);+0:1]=[O+0:4].[C;!$(*(=O)=O);+0:2]=[O+0:5])>>[*:1]=[*:2].[*:4]=[*:5]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Olefin Metathesis
    # Cross Metathesis (CM)
    OperatorSmarts(
        "Olefin Cross Metathesis (CM)",
        "[C+0:1]=!@[C+0:2].[C+0:3]=!@[C+0:4]>>[*:1]=[*:3].[*:2]=[*:4]",
        (1, 1),
        (1, 1),
    ),
    # Ring-Opening Metathesis (ROM)
    # Ring-Opening Metathesis 1: will produce incorrect products along with correct products, a stoichiometry filter can help
    OperatorSmarts(
        "Olefin Ring-Opening Metathesis (ROM) 1",
        "([C+0:1]=!@[C+0:3].[C+0:2]=!@[C+0:4])>>[*:1]=[*:2].[*:3]=[*:4]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Ring-Opening Metathesis 2: skip, don't know how to map identical but not same groups
    #    OperatorSmarts("Olefin Ring-Opening Metathesis (ROM) 2",
    #                   "",
    #                   ( , ),( ,  )),
    # Ring-Closing Metathesis (RCM)
    OperatorSmarts(
        "Olefin Ring-Closing Metathesis (RCM)",
        "[C+0:1]=@[C+0:2].[C+0:3]=!@[C+0:4]>>([*:1]=[*:3].[*:2]=[*:4])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Reductive Cross-Coupling of Alkenes https://www.nature.com/articles/nature14006 https://www.nature.com/articles/s41467-022-30286-8
    OperatorSmarts(
        "Reductive Cross-Coupling of Alkenes",
        "[C+0!H0:1][C+0:2]-!@[C+0:3][C+0!H0:4]>>[*:1]=[*:2].[*:3]=[*:4].[H][H]",
        (1,),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Epoxidation of Alkene
    OperatorSmarts(
        "Epoxidation of Alkene",
        "[C+0:1]1[C+0:2][O+0:3]1>>[*:1]=[*:2].[*:3]=[O]",
        (1,),
        (1, 0.5),
        Retro_Not_Aromatic=True,
    ),
    # Hydration of Alkene, Ethers from Addition of Alcohols or Acids to Alkenes
    OperatorSmarts(
        "Hydration of Alkene, Addition of Alcohols or Acids to Alkenes",
        "[C+0!H0:1][C!$(*=O)+0:2]-!@[O+0:3]>>[*:1]=[*:2].[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Addition of Alcohols or Acids to Alkenes, Intramolecular",
        "[C+0!H0:1][C!$(*=O)+0:2]-@[O+0:3][C+0:4]>>([*:1]=[*:2].[*:3][*:4])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Hydration of Alkenes, 2-step
    OperatorSmarts(
        "Hydration of Alkenes, 2-step",
        "([C+0!H0:1][C+0:2][O+0H:5].[C+0!H0:3][C+0:4][O+0H])>>([*:1]=[*:2].[*:3]=[*:4]).[*:5]",
        (1,),
        (1, 2),
        number_of_steps=2,
        Retro_Not_Aromatic=True,
    ),
    # Hydrohalogenation of Alkenes
    OperatorSmarts(
        "Hydrohalogenation of Alkenes",
        "[C+0!H0:1][C+0:2][F,Cl,Br,I;+0:3]>>[*:1]=[*:2].[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Halogenation of Alkenes
    OperatorSmarts(
        "Halogenation of Alkenes",
        "[C+0:1]([F,Cl,Br,I;+0:3])[C+0:2][F,Cl,Br,I;+0:4]>>[*:1]=[*:2].[*:3][*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Diels-Alder Reaction   may generate a smiles with fragments within it, ring_issue filter checks it
    OperatorSmarts(
        "Diels-Alder Reaction with Alkenes",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][C+0:6][C+0:5]1>>[*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6]",
        (1,),
        (1, 1),
        ring_issue=True,
    ),
    OperatorSmarts(
        "Diels-Alder Reaction with Alkenes, Intramolecular",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][C+0:6][C+0:5]1>>([*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6])",
        (1,),
        (1,),
        ring_issue=True,
    ),
    OperatorSmarts(
        "Diels-Alder Reaction with Alkynes",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][C+0:6]=[C+0:5]1>>[*:1]=[*:2][*:3]=[*:4].[*:5]#[*:6]",
        (1,),
        (1, 1),
        ring_issue=True,
    ),
    OperatorSmarts(
        "Diels-Alder Reaction with Alkynes, Intramolecular",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][C+0:6]=[C+0:5]1>>([*:1]=[*:2][*:3]=[*:4].[*:5]#[*:6])",
        (1,),
        (1,),
        ring_issue=True,
    ),
    # Oxo-Diels-Alder Reaction
    OperatorSmarts(
        "Oxo-Diels-Alder Reaction",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][O+0:6][CX4!$(*(-O)-O)!$(*(-O)(-O)-O)+0:5]1>>[*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Oxo-Diels-Alder Reaction, Intramolecular",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4][O+0:6][CX4!$(*(-O)-O)!$(*(-O)(-O)-O)+0:5]1>>([*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6])",
        (1,),
        (1,),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Acrolein Diels-Alder Reaction
    OperatorSmarts(
        "Acrolein Diels-Alder Reaction",
        "[C+0:1]1[C+0:2]=[C!$(*(-O)-O)+0:3][O+0:4][C+0:6][C+0:5]1>>[*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Acrolein Diels-Alder Reaction, Intramolecular",
        "[C+0:1]1[C+0:2]=[C!$(*(-O)-O)+0:3][O+0:4][C+0:6][C+0:5]1>>([*:1]=[*:2][*:3]=[*:4].[*:5]=[*:6])",
        (1,),
        (1,),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Halohydrin Formation
    OperatorSmarts(
        "Halohydrin Formation",
        "[C+0:1]([O+0H:5])[C+0:2][F,Cl,Br,I;+0:3].[F,Cl,Br,I;+0H:4]>>[*:1]=[*:2].[*:3][*:4].[*:5]",
        (1, 1),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Diol Formation by Oxidation
    OperatorSmarts(
        "Diol Formation by Oxidation",
        "[C+0:1]([O+0H:3])[C+0:2][O+0H:4]>>[*:1]=[*:2].[*:3]=[O].[*:4]",
        (1,),
        (1, 0.5, 1),
        Retro_Not_Aromatic=True,
    ),
    # Conjugated Dienes 1,4 Addition
    OperatorSmarts(
        "Conjugated Dienes 1,4 Addition with Hydrogen Halide",
        "[F,Cl,Br,I;+0:5][C+0:1][C+0:2]=[C+0:3][C+0!H0:4]>>[*:1]=[*:2][*:3]=[*:4].[*:5]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Conjugated Dienes 1,4 Addition with Halogens",
        "[F,Cl,Br,I;+0:5][C+0:1][C+0:2]=[C+0:3][C+0:4][F,Cl,Br,I;+0:6]>>[*:1]=[*:2][*:3]=[*:4].[*:5][*:6]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Claisen Rearrangement, Cope Rearrangements                 [:1] and [:6] shouldn't connect, use filter
    OperatorSmarts(
        "Claisen Rearrangement, Cope Rearrangements",
        "[O,C;+0:1]=[C+0:2][C+0:3][C+0:4][C+0:5]=[C+0:6]>>[*:3]=[*:2][*:1][*:6][*:5]=[*:4]",
        (1,),
        (1,),
        ring_issue=True,
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    # Aromatic Claisen Rearrangement    should use kekulize_flag for new aromatic ring but need to rewrite it first
    OperatorSmarts(
        "Aromatic Claisen Rearrangement 1",
        "[c+0:1]1([C+0:10][C+0:9]=[C+0:8]):[c+0:2]:[c+0:3]:[c+0:4]:[c+0:5]:[c+0:6]:1-[O+0H:7]>>[*:1]1:[*:2]:[*:3]:[*:4]:[*:5]:[*:6]:1-[*:7][*:8][*:9]=[*:10]",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Aromatic Claisen Rearrangement with Ortho Substituents",
        "[c+0H0:1]1:[c+0:2]:[c+0:3]([C+0:8][C+0:9]=[C+0:10]):[c+0:4]:[c+0H0:5]:[c+0:6]:1-[O+0H:7]>>[*:1]1:[*:2]:[*:3]:[*:4]:[*:5]:[*:6]:1-[*:7][*:8][*:9]=[*:10]",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # other Claisen Rearrangement Variations/Sigmatropic reaction
    # Tsuji–Trost Reaction
    # Nu = Active Methylenes
    OperatorSmarts(
        "Tsuji–Trost Reaction, Nu = Active Methylenes",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-!@[C+0:7]([C+0:5]=[O+0:6])[C+0:8]=[O+0:9].[F,Cl,Br,I,O$(*C=O);+0H:4]>>[*:1]=[*:2][*:3][*:4].[*:5](=[*:6])[*:7][*:8]=[*:9]",
        (1, 1),
        (1, 1),
    ),
    # Nu = Enolates
    OperatorSmarts(
        "Tsuji–Trost Reaction, Nu = Enolates",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-!@[C+0:7]([C+0:5])[C+0:8]=[O+0:9].[F,Cl,Br,I,O$(*C=O);+0H:4]>>[*:1]=[*:2][*:3][*:4].[*:5][*:7][*:8]=[*:9]",
        (1, 1),
        (1, 1),
    ),
    # Nu = Amines
    OperatorSmarts(
        "Tsuji–Trost Reaction, Nu = Amines",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-!@[N+0:7][C,c;+0:8].[F,Cl,Br,I,O$(*C=O);+0H:4]>>[*:1]=[*:2][*:3][*:4].[*:7][*:8]",
        (1, 1),
        (1, 1),
    ),
    # Nu = Phenols
    OperatorSmarts(
        "Tsuji–Trost Reaction, Nu = Phenols",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-!@[O+0:7][c+0:8].[F,Cl,Br,I,O$(*C=O);+0H:4]>>[*:1]=[*:2][*:3][*:4].[*:7][*:8]",
        (1, 1),
        (1, 1),
    ),
    # Intramolecular versions
    # Intramolecular Tsuji-Trost Reaction, Nu = Active Methylenes
    OperatorSmarts(
        "Intramolecular Tsuji-Trost Reaction, Nu = Active Methylenes",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-@[C+0:7]([C+0:5]=[O+0:6])[C+0:8]=[O+0:9].[F,Cl,Br,I,O$(*C=O);+0H:4]>>([*:1]=[*:2][*:3][*:4].[*:5](=[*:6])[*:7][*:8]=[*:9])",
        (1, 1),
        (1,),
    ),
    # Intramolecular Tsuji-Trost Reaction, Nu = Enolates
    OperatorSmarts(
        "Intramolecular Tsuji-Trost Reaction, Nu = Enolates",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-@[C+0:7]([C+0:5])[C+0:8]=[O+0:9].[F,Cl,Br,I,O$(*C=O);+0H:4]>>([*:1]=[*:2][*:3][*:4].[*:5][*:7][*:8]=[*:9])",
        (1, 1),
        (1,),
    ),
    # Intramolecular Tsuji-Trost Reaction, Nu = Amines
    OperatorSmarts(
        "Intramolecular Tsuji-Trost Reaction, Nu = Amines",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-@[N+0:7][C,c;+0:8].[F,Cl,Br,I,O$(*C=O);+0H:4]>>([*:1]=[*:2][*:3][*:4].[*:7][*:8])",
        (1, 1),
        (1,),
    ),
    # Intramolecular Tsuji-Trost Reaction, Nu = Phenols
    OperatorSmarts(
        "Intramolecular Tsuji-Trost Reaction, Nu = Phenols",
        "[C+0:1]=[C+0:2][C+0;!$(*[OH]);!$(*=O):3]-@[O+0:7][c+0:8].[F,Cl,Br,I,O$(*C=O);+0H:4]>>([*:1]=[*:2][*:3][*:4].[*:7][*:8])",
        (1, 1),
        (1,),
    ),
    # Oxychlorination
    OperatorSmarts(
        "Oxychlorination",
        "[C+0:1]([F,Cl,Br,I;+0:3])[C+0:2][F,Cl,Br,I;+0].[O+0H2:4]>>[*:1]=[*:2].[*:3].[*:4]=[O]",
        (1, 1),
        (1, 2, 0.5),
        Retro_Not_Aromatic=True,
    ),
    # Acetoxylation of Alkenes
    OperatorSmarts(
        "Acetoxylation of Alkenes",
        "[C+0:3](=[O+0:4])[O+0:5]-!@[C+0:1]=[C+0:2].[O+0H2:6]>>[*:1]=[*:2].[*:3](=[*:4])[*:5].[*:6]=[O]",
        (1, 1),
        (1, 1, 0.5),
    ),
    OperatorSmarts(
        "Acetoxylation of Alkenes, Intramolecular",
        "[C+0:3](=[O+0:4])[O+0:5]-@[C+0:1]=[C+0:2].[O+0H2:6]>>([*:1]=[*:2].[*:3](=[*:4])[*:5]).[*:6]=[O]",
        (1, 1),
        (1, 0.5),
    ),  # does not work for O=C1OC=CC=C1 unless add kekulize_flag
    # Oxidation of Propene
    OperatorSmarts(
        "Oxidation of Propene",
        "[C+0H2:1]=[C+0H:2][C+0H:3]=[O+0:4].[O+0H2:5]>>[*:1]=[*:2][*:3].[*:4]=[*:5]",
        (1, 1),
        (1, 1),
    ),
    # Alkynes ##############################################################
    # Halogen Addition of Alkynes
    OperatorSmarts(
        "Halogen Addition of Alkynes",
        "[C+0:1]([F,Cl,Br,I;+0:3])=[C+0:2][F,Cl,Br,I;+0:4]>>[*:1]#[*:2].[*:3][*:4]",
        (1,),
        (1, 1),
    ),
    # Hydrogen Halides Addition of Alkynes
    OperatorSmarts(
        "Hydrogen Halides Addition of Alkynes",
        "[C+0:1]([F,Cl,Br,I;+0:3])=[C+0!H0:2]>>[*:1]#[*:2].[*:3]",
        (1,),
        (1, 1),
    ),
    # Hydration of Alkynes
    OperatorSmarts(
        "Hydration of Alkynes",
        "[C+0:1]([O+0H:3])=[C+0!H0:2]>>[*:1]#[*:2].[*:3]",
        (1,),
        (1, 1),
    ),
    # Hydrogenation of Alkynes
    OperatorSmarts(
        "Hydrogenation of Alkynes",
        "[C+0!H0:1]=[C+0!H0:2]>>[*:1]#[*:2].[H][H]",
        (1,),
        (1, 1),
    ),
    OperatorSmarts(
        "Hydrogenation of Alkynes to Alkanes",
        "[C;H2,H3;+0:1][C;H2,H3;+0:2]>>[*:1]#[*:2].[H][H]",
        (1,),
        (1, 2),
    ),
    # Gentle Alkyne Oxidation
    OperatorSmarts(
        "Gentle Alkyne Oxidation",
        "[C+0:1](=[O+0:4])[C+0:2]=[O+0:5]>>[*:1]#[*:2].[*:4]=[*:5]",
        (1,),
        (1, 1),
    ),
    # Oxidative Cleavage of Alkynes
    OperatorSmarts(
        "Oxidative Cleavage of Alkynes",
        "[*:6][C+0:1](=[O+0:3])[O+0H:4].[*:7][C+0:2](=[O+0:5])[O+0H]>>[*:6][*:1]#[*:2][*:7].[*:3].[*:4]=[*:5]",
        (1, 1),
        (1, 1, 1.5),
    ),
    OperatorSmarts(
        "Oxidative Cleavage of Alkynes Intramolecular",
        "([*:6][C+0:1](=[O+0:3])[O+0H:4].[*:7][C+0:2](=[O+0:5])[O+0H])>>[*:6][*:1]#[*:2][*:7].[*:3].[*:4]=[*:5]",
        (1,),
        (1, 1, 1.5),
    ),
    OperatorSmarts(
        "Oxidative Cleavage of Terminal Alkynes",
        "[*:6][C+0:1](=[O+0:4])[O+0H:5].[O]=[C+0:2]=[O]>>[*:6][*:1]#[*:2].[*:4]=[*:5]",
        (1, 1),
        (1, 2),
    ),
    # Alkynes by Dehydrohalogenation
    OperatorSmarts(
        "Alkynes by Dehydrohalogenation of Alkanes",
        "[C+0:1]#[C+0:3].[F,Cl,Br,I;+0H:2]>>[*:1]([*:2])[*:3]([*:2])",
        (1, 2),
        (1,),
    ),
    OperatorSmarts(
        "Alkynes by Dehydrohalogenation of Alkenes",
        "[C+0:1]#[C+0:3].[F,Cl,Br,I;+0H:2]>>[*:1]([*:2])=[*:3]",
        (1, 1),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Alkylation of Acetylide Anions with Methyl and Primary Haloalkanes
    # could add an enthalpy correction term to account for effect of NaNH2, but probably unnecessary since dH < 0 for tested cases
    # enthalpy correction from DFT: NaNH2 -> NH3 + NaBr - HBr  dH = -54.50 kcal/mol
    OperatorSmarts(
        "Alkylation of Acetylide Anions with Methyl and Primary Haloalkanes",
        "[C+0:1]#[C+0:2]-!@[C;H2,H3;+0:4].[F,Cl,Br,I;+0H:3]>>[*:1]#[*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
        enthalpy_correction=-54.50,
    ),  # DFT by QE
    # Sonogashira Coupling, Acyl Sonogashira Coupling
    OperatorSmarts(
        "Sonogashira Coupling",
        "[C+0:1]#[C+0:2]-!@[c,C$(*=C),C$(*=O);+0:4].[F,Cl,Br,I;+0H:3]>>[*:1]#[*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    # Addition of Alkynes to Aldehydes and Activated Ketones   doi.org/10.1021/ol026282k  doi.org/10.1021/jo701643h
    OperatorSmarts(
        "Addition of Alkynes to Aldehydes",
        "[C+0:1]#[C+0:2]-!@[C+0!H0:3][O+0H:4]>>[*:1]#[*:2].[*:3]=[*:4]",
        (1,),
        (1, 1),
    ),
    OperatorSmarts(
        "Addition of Alkynes to Aldehydes, Intramolecular",
        "[C+0:1]#[C+0:2]-@[C+0!H0:3][O+0H:4]>>([*:1]#[*:2].[*:3]=[*:4])",
        (1,),
        (1,),
    ),
    OperatorSmarts(
        "Addition of Alkynes to Activated Ketones",
        "[C+0:1]#[C+0:2]-!@[C!$(*(O)O)+0:3]([O+0H:4])[C$(*=O)+0:5]>>[*:1]#[*:2].[*:5][*:3]=[*:4]",
        (1,),
        (1, 1),
    ),
    # Haloalkanes, Halogenation ###########################################
    # Alcohols React with Hydrogen Halides to form Haloalkanes, Carboxylic Acids Conversion to Acid Chlorides
    OperatorSmarts(
        "Alcohols React with Hydrogen Halides to form Haloalkanes, Carboxylic Acids Conversion to Acid Chlorides",
        "[C+0:1][F,Cl,Br,I;+0:3].[O+0H2:2]>>[*:1][*:2].[*:3]",
        (1, 1),
        (1, 1),
    ),
    # Haloalkane Hydrolysis, Acid Chlorides Hydrolysis, Haloarenes Hydrolysis
    OperatorSmarts(
        "Haloalkane Hydrolysis, Acid Chlorides Hydrolysis, Haloarenes Hydrolysis",
        "[C,c;+0:1][O+0H:2].[F,Cl,Br,I;+0H:3]>>[*:1][*:3].[*:2]",
        (1, 1),
        (1, 1),
    ),
    # Wurtz Reaction, Coupling of Halides with Gilman Reagent                  may need enthalpy correction
    OperatorSmarts(
        "Wurtz Reaction, Coupling of Halides with Gilman Reagent",
        "[C,c;+0:1]-!@[C,c;+0:3].[F,Cl,Br,I;+0:2][F,Cl,Br,I;+0:4]>>[*:1][*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Wurtz Reaction, Coupling of Halides with Gilman Reagent, Intramolecular",
        "[C,c;+0:1]-@[C,c;+0:3].[F,Cl,Br,I;+0:2][F,Cl,Br,I;+0:4]>>([*:1][*:2].[*:3][*:4])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Dehydrohalogenation
    OperatorSmarts(
        "Dehydrohalogenation",
        "[C+0:1]=[C+0:3].[F,Cl,Br,I;+0H:2]>>[*:1]([*:2])[*:3]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Aromatic Halogenation
    OperatorSmarts(
        "Aromatic Halogenation",
        "[c+0:1][F,Cl,Br,I;+0:2].[F,Cl,Br,I;+0H:3]>>[*:1].[*:2][*:3]",
        (1, 1),
        (1, 1),
    ),
    # Friedel–Crafts Reaction        does not work for alkenyl/alkynyl halides
    OperatorSmarts(
        "Friedel–Crafts Reaction",
        "[c+0:1]-!@[CX4,C$(*=O);+0:2].[F,Cl,Br,I;+0H:3]>>[*:1].[*:2][*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Friedel–Crafts Reaction, Intramolecular",
        "[c+0:1]-@[CX4,C$(*=O);+0:2].[F,Cl,Br,I;+0H:3]>>([*:1].[*:2][*:3])",
        (1, 1),
        (1,),
    ),  # might use kekulize flag for products like O=c1occc2ccccc12? but would need to rewrite
    OperatorSmarts(
        "Friedel–Crafts Acylation with Carboxylic Acids",  # doi.org/10.1021/ol800752v
        "[c+0:1]-!@[C$(*=O)+0:2].[O+0H2:3]>>[*:1].[*:2][*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Friedel–Crafts Acylation with Carboxylic Acids, Intramolecular",
        "[c+0:1]-@[C$(*=O)+0:2].[O+0H2:3]>>([*:1].[*:2][*:3])",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Friedel–Crafts Acylation with Acid Anhydrides",
        "[c+0:1]-!@[C$(*=O)+0:2].[O+0H:3][C$(*=O)+0:4]>>[*:1].[*:2][*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Friedel–Crafts Acylation with Acid Anhydrides, Intramolecular",
        "[c+0:1]-@[C$(*=O)+0:2].[O+0H:3][C$(*=O)+0:4]>>([*:1].[*:2][*:3][*:4])",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Friedel–Crafts Reaction with Alkenes",
        "[c+0:1]-!@[C+0:2][C+0!H0:3]>>[*:1].[*:2]=[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Friedel–Crafts Reaction with Alkenes, Intramolecular",
        "[c+0:1]-@[C+0:2][C+0!H0:3]>>([*:1].[*:2]=[*:3])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Heck Reaction      doi.org/10.1039/C4CC00297K
    OperatorSmarts(
        "Heck Reaction 1",
        "[C+0:1]=[C+0:2]-!@[c+0:3].[F,Cl,Br,I;+0H:4]>>[*:1]=[*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Heck Reaction 2",
        "[c+0:5][C+0:1]=[C+0:2]-!@[C,c;+0:3].[F,Cl,Br,I;+0H:4]>>[*:5][*:1]=[*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Heck Reaction 1, Intramolecular",
        "[C+0:1]=[C+0:2]-@[c;+0:3].[F,Cl,Br,I;+0H:4]>>([*:1]=[*:2].[*:3][*:4])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Heck Reaction 2, Intramolecular",
        "[c+0:5][C+0:1]=[C+0:2]-@[C,c;+0:3].[F,Cl,Br,I;+0H:4]>>([*:5][*:1]=[*:2].[*:3][*:4])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Suzuki Coupling (Combined with Grignard Reagent and Borate Ester Formation, or Hydroboration of Alkenes or Alkynes)
    # NOT BALANCED, needs to add a correction term for enthalpy calculation
    # Boranes from R-X
    # enthalpy correction from DFT: Mg + B(OCH3)3 -> BrMgOCH3 + B(OCH3)2Br  dH = -42.13 kcal/mol
    # similar to Wurtz reaction but more strict on reactants. Not sure if intramolecular possible for Suzuki coupling
    OperatorSmarts(
        "Suzuki Coupling with Boranes from Alkyl, Alkenyl, or Aryl Halides",
        "[c,C!$(*~O);!$(*#*);+0:1]-!@[c,C$(*=,#C);+0:2]>>[*:1][Br].[*:2][Br]",
        (1,),
        (1, 1),
        enthalpy_correction=-42.13,
    ),  # DFT by QE
    # Boranes from alkenes or alkynes
    # enthalpy correction from DFT: (Sia)2BH -> (Sia)2BBr   dH = -26.11 kcal/mol
    OperatorSmarts(
        "Suzuki Coupling with Boranes from Alkenes",
        "[C+0!H0:1]-[C+0:2]-!@[c,C$(*=,#C);+0:3]>>[*:1]=[*:2].[*:3][Br]",
        (1,),
        (1, 1),
        enthalpy_correction=-26.11,  # DFT by QE
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Suzuki Coupling with Boranes from Alkynes",
        "[C+0!H0:1]=[C+0:2]-!@[c,C$(*=,#C);+0:3]>>[*:1]#[*:2].[*:3][Br]",
        (1,),
        (1, 1),
        enthalpy_correction=-26.11,
    ),  # DFT by QE
    # Reduction of Haloalkanes
    OperatorSmarts(
        "Reduction of Haloalkanes",
        "[CX4,c;+0!H0:1].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[H][H]",
        (1, 1),
        (1, 1),
    ),
    # Grignard Reagent with Oxiranes
    # NOT BALANCED, needs to add a correction term for enthalpy calculation
    # enthalpy correction from DFT: Mg + HBr -> MgBr2  dH = -61.15
    OperatorSmarts(
        "Grignard Reagent with Oxiranes",
        "[c,C!$(*~O);!$(*#*);+0:1][C+0!R:2][C+0!R:3][O+0H:4]>>[*:1][Br].[*:2]1[*:3][*:4]1",
        (1,),
        (1, 1),
        enthalpy_correction=-61.15,
    ),  # DFT by QE
    # Dichlorocarbene with Alkenes
    OperatorSmarts(
        "Dichlorocarbene with Alkenes",
        "[C+0:1]1([F,Cl,Br,I;+0:2])([F,Cl,Br,I;+0:3])[C+0:5][C+0:6]1.[F,Cl,Br,I;+0H:4]>>[*:1]([*:2])([*:3])[*:4].[*:5]=[*:6]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Simmons-Smith Reaction           not balanced
    OperatorSmarts(
        "Simmons-Smith Reaction",
        "[C+0H2:1]1[C+0:5][C+0:6]1.[F,Cl,Br,I;+0H:2]>>[*:1]([*:2])[*:2].[*:5]=[*:6]",
        (1, 2),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Esterification with Alkyl and Aryl Halides                         aryl:doi.org/10.1021/acs.joc.1c00204
    OperatorSmarts(
        "Esterification with Alkyl and Aryl Halides",
        "[C+0:2](=[O+0:3])[O+0:4]!@[CX4,c;+0:5].[F,Cl,Br,I;+0H:6]>>[*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Esterification with Alkyl and Aryl Halides, Intramolecular",
        "[C+0:2](=[O+0:3])[O+0:4]@[CX4,c;+0:5].[F,Cl,Br,I;+0H:6]>>([*:2](=[*:3])[*:4].[*:5][*:6])",
        (1, 1),
        (1,),
    ),
    # Allylic, Benzylic Halogenation (Wohl–Ziegler Reaction)
    OperatorSmarts(
        "Allylic, Benzylic Halogenation",
        "[C$(*=C),c;+0:1][CX4!$(*~[O,N,S])+0:2][F,Cl,Br,I;+0:3].[F,Cl,Br,I;+0H:4]>>[*:1][*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    # Phosgene Production
    OperatorSmarts(
        "Phosgene Production",
        "[F,Cl,Br,I;+0:3][C+0](=[O+0])[F,Cl,Br,I;+0:4]>>[C-]#[O+].[*:3][*:4]",
        (1,),
        (1, 1),
    ),
    # Enolate Alkylation
    # From James Gerken: it doesn't really form HX as a product but rather MX
    # and the protonated form of whatever base was used to deprotonate alpha to the carbonyl.
    # Estimated difference in DMSO pKa between RC(=O)C-H and H-Br, should be about -33 kcal/mol
    OperatorSmarts(
        "Enolate Alkylation",
        "[C+0:2](=[O+0:3])[C+0:4]!@[CX4;+0:5].[F,Cl,Br,I;+0H:6]>>[*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
        enthalpy_correction=-33,
    ),
    OperatorSmarts(
        "Enolate Alkylation, Intramolecular",
        "[C+0:2](=[O+0:3])[C+0:4]@[CX4;+0:5].[F,Cl,Br,I;+0H:6]>>([*:2](=[*:3])[*:4].[*:5][*:6])",
        (1, 1),
        (1,),
        enthalpy_correction=-33,
    ),
    # Alcohols #############################################################
    # Glycol Cleavage by Oxidation
    OperatorSmarts(
        "Glycol Cleavage by Oxidation",
        "[C!$(*(=O)=O)+0:1]=[O+0:5].[C!$(*(=O)=O)+0:2]=[O+0:6].[O+0H2:3]>>[*:1]([*:5])[*:2][*:6].[*:3]=[O]",
        (1, 1, 1),
        (1, 0.5),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Glycol Cleavage by Oxidation Intramolecular",
        "([C+0:1]=[O+0:5].[C+0:2]=[O+0:6]).[O+0H2:3]>>[*:1]([*:5])[*:2][*:6].[*:3]=[O]",
        (1, 1),
        (1, 0.5),
        ring_issue=True,
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    # Hydrodeoxygenation of Alcohol, Classic Synthesis of Aldehydes from Carboxylic Acids
    OperatorSmarts(
        "Hydrodeoxygenation of Alcohol, Classic Synthesis of Aldehydes from Carboxylic Acids",
        "[C,c;+0!H0:1].[O+0H2:2]>>[*:1][*:2].[H][H]",
        (1, 1),
        (1, 1),
    ),
    # Dehydration of Alcohols
    OperatorSmarts(
        "Dehydration of Alcohol",
        "[C+0:1]=[C+0:2].[O+0H2:3]>>[*:1][*:2][*:3]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Dehydration of Alcohols, 2-step
    OperatorSmarts(
        "Dehydration of Alcohol, 2-step",
        "([C+0:1]=[C+0:2].[C+0:4]=[C+0:5]).[O+0H2:3]>>([*:1][*:2][*:3].[*:4][*:5][O])",
        (1, 2),
        (1,),
        kekulize_flag=True,
        number_of_steps=2,
    ),
    # Selective Oxidation of Alcohols
    OperatorSmarts(
        "Selective Oxidation of Alcohols",
        "[C+0:1]=[O+0:2].[O+0H2:3]>>[*:1][*:2].[*:3]=[O]",
        (1, 1),
        (1, 0.5),
        kekulize_flag=True,
    ),
    # Diol Carboxylation
    OperatorSmarts(
        "Diol Carboxylation",
        "[O+0H2:1].[C+0:2]1[C+0:3][O+0:4][C+0:6](=[O+0:7])[O+0:5]1>>[*:1][*:2][*:3][*:4].[*:5]=[*:6]=[*:7]",
        (1, 1),
        (1, 1),
    ),
    # add n=1, doi.org/10.1021/cs500301d
    OperatorSmarts(
        "Diol Carboxylation 2",
        "[O+0H2:1].[C+0:2]1[C+0:8][C+0:3][O+0:4][C+0:6](=[O+0:7])[O+0:5]1>>[*:1][*:2][*:8][*:3][*:4].[*:5]=[*:6]=[*:7]",
        (1, 1),
        (1, 1),
    ),
    # Hydrogenolysis of Primary Alcohol                 doi:10.1021/ja01330a506
    OperatorSmarts(
        "Hydrogenolysis of Primary Alcohol",
        "[C+0!H0:1].[C+0H4:3].[O+0H2:2]>>[*:1][*:3][*:2].[H][H]",
        (1, 1, 1),
        (1, 2),
    ),
    # Pinacol Rearrangement               might want to restrict number of Hs on the right side as well
    # no H on C2
    OperatorSmarts(
        "Pinacol Rearrangement, no H on Carbon#2",
        "[C+0:1][C+0:2](=[O+0:4])[C+0X4:5][C+0:3].[O+0H2:8]>>[*:1][*:2]([*:3])([*:4])[*:5][*:8]",
        (1, 1),
        (1,),
    ),
    # 1 H on C2    https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Book%3A_Virtual_Textbook_of_OChem_%28Reusch%29_UNDER_CONSTRUCTION/30%3A_Cationic_Rearrangements/30.2%3A_Pinacol_Rearrangement
    OperatorSmarts(
        "Pinacol Rearrangement, 1 H on Carbon#2",
        "[C+0:3][C+0:2](=[O+0:4])[C+0X4!H0:5].[O+0H2:8]>>[*:2]([*:3])([*:4])[*:5][*:8]",
        (1, 1),
        (1,),
    ),
    # 2 Hs on C2
    OperatorSmarts(
        "Pinacol Rearrangement, 2 Hs on Carbon#2",
        "[C+0H:2](=[O+0:4])[C+0X4!H0:5].[O+0H2:8]>>[*:2]([*:4])[*:5][*:8]",
        (1, 1),
        (1,),
    ),
    # Dehydration of Geminal Diol
    OperatorSmarts(
        "Dehydration of Geminal Diol",
        "[C;!$(*[OH]);+0:1]=[O+0:2].[O+0H2:3]>>[*:1]([*:2])[*:3]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Formation of Acetals from Hemiacetals
    OperatorSmarts(
        "Formation of Acetals from Hemiacetals",
        "[C+0X4:1]([O+0H0X2:2])[O+0:4]!@[C+0X4:5].[O+0H2:3]>>[*:1]([*:2])[*:3].[*:4][*:5]",
        (1, 1),
        (1, 1),
    ),
    # Oxidation Of Primary Alcohols to Carboxylic Acids
    OperatorSmarts(
        "Oxidation Of Primary Alcohols to Carboxylic Acids",
        "[C+0:1](=[O+0:3])[O+0H:2].[O+0H2:4]>>[*:1][*:2].[*:3]=[*:4]",
        (1, 1),
        (1, 1),
    ),
    # Oxidation Of Primary Alcohols to Carboxylic Acids, 2-step
    OperatorSmarts(
        "Oxidation Of Primary Alcohols to Carboxylic Acids, 2-step",
        "([C+0:1](=[O+0:3])[O+0H:2].[C+0:5](=[O+0:6])[O+0H]).[O+0H2:4]>>([*:1][*:2].[*:5][*:6]).[*:3]=[*:4]",
        (1, 2),
        (1, 2),
        number_of_steps=2,
    ),
    # Formation of Cyclic Acetals from Ketones/Aldehydes with Diols
    OperatorSmarts(
        "Formation of Cyclic Acetals from Ketones/Aldehydes with Diols",
        "[C+0X4!$(*(O)(O)O)!$(*(O)(O)(O)O):1]1[O+0:3][C+0X4:4][C+0X4:5][O+0:6]1.[O+0H2:2]>>[*:1]=[*:2].[*:3][*:4][*:5][*:6]",
        (1, 1),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Oxidation of Cyclohexane
    OperatorSmarts(
        "Oxidation of Cyclohexane 1",
        "[C+0H2:1]1[C+0H2:2][C+0H2:3][C+0H2:4][C+0H2:5][C+0H:6]1[O+0H:7]>>[*:1]1[*:2][*:3][*:4][*:5][*:6]1.[*:7]=[O]",
        (1,),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Oxidation of Cyclohexane 2",
        "[C+0H2:1]1[C+0H2:2][C+0H2:3][C+0H2:4][C+0H2:5][C+0:6]1=[O+0:7].[O+0H2:8]>>[*:1]1[*:2][*:3][*:4][*:5][*:6]1.[*:7]=[*:8]",
        (1, 1),
        (1, 1),
    ),
    # Methanol from Syngas
    OperatorSmarts(
        "Methanol from Syngas", "[C+0H3][O+0H]>>[C-]#[O+].[H][H]", (1,), (1, 2)
    ),
    # Ethers, Epoxides ####################################################
    # Hydrolysis of Ethers, Esters, Anhydrides                          https://www.masterorganicchemistry.com/reaction-guide/acidic-cleavage-of-ethers-sn2-reaction/   Ar-O-Ar stable but possible: doi.org/10.1016/j.jcat.2013.09.012
    OperatorSmarts(
        "Hydrolysis of Ethers, Esters, Anhydrides",
        "[C,c;+0:1][O+0H:2].[C,c;+0:3][O+0H:4]>>[*:1][*:2][*:3].[*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Hydrolysis of Ethers, Esters, Anhydrides, Intramolecular",
        "([C,c;+0:1][O+0H:2].[C,c;+0:3][O+0H:4])>>[*:1][*:2][*:3].[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Hydrogenolysis of Ethers
    OperatorSmarts(
        "Hydrogenolysis of Ethers",
        "[C,c;+0!H0;!$(*=O):1].[O+0H:2][C,c;+0;!$(*=O):3]>>[*:1][*:2][*:3].[H][H]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Hydrogenolysis of Ethers Intramolecular",
        "([C,c;+0!H0;!$(*=O):1].[O+0H:2][C,c;+0;!$(*=O):3])>>[*:1][*:2][*:3].[H][H]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Williamson Ether Synthesis, Ullmann Condensation           doesn't work with tertiary alkyl halides or alkenyl or alkynyl halide
    OperatorSmarts(
        "Williamson Ether Synthesis, Ullmann Condensation",
        "[C,c;!$(*=O);+0:1][O+0:2]!@[CX4!H0,c;+0:3].[F,Cl,Br,I;+0H:4]>>[*:1][*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Williamson Ether Synthesis, Ullmann Condensation, Intramolecular",
        "[C,c;!$(*=O);+0:1][O+0:2]@[CX4!H0,c;+0:3].[F,Cl,Br,I;+0H:4]>>([*:1][*:2].[*:3][*:4])",
        (1, 1),
        (1,),
    ),
    # Ether Cleavage                             Ar-O-R + HI -> Ar-OH + IR; Ar-O-Ar stable
    OperatorSmarts(
        "Ether Cleavage",
        "[C,c;+0;!$(*=O):1][O+0H:2].[C;+0;!$(*=O):3][F,Cl,Br,I;+0:4]>>[*:1][*:2][*:3].[*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Ether Cleavage, Intramolecular",
        "([C,c;+0;!$(*=O):1][O+0H:2].[C;+0;!$(*=O):3][F,Cl,Br,I;+0:4])>>[*:1][*:2][*:3].[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Ether Synthesis by Dehydration       tertiary alcohols dehydration to alkenes
    OperatorSmarts(
        "Ether Synthesis by Dehydration",
        "[C,c;!$(*=O);+0:1][O+0:2]!@[C,c;!$(*=O);+0:3].[O+0H2:4]>>[*:1][*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Ether Synthesis by Dehydration, Intramolecular",
        "[C,c;!$(*=O);+0:1][O+0:2]@[C,c;!$(*=O);+0:3].[O+0H2:4]>>([*:1][*:2].[*:3][*:4])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Epoxides Ring Opening
    OperatorSmarts(
        "Epoxides Ring Opening",
        "[O+0;!$(*-C=O):4][C+0:1][C+0:2][O+0H:3]>>[*:1]1[*:2][*:3]1.[*:4]",
        (1,),
        (1, 1),
        ring_issue=True,
    ),
    # Organometallic ######################################################
    # Transmetalation
    # Aldehydes and Ketones ###############################################
    # Aldehyde Oxidation
    OperatorSmarts(
        "Aldehyde Oxidation",
        "[C!$(*([OH])[OH])+0:1](=[O+0:2])[O+0H:3]>>[*:1]=[*:2].[*:3]=[O]",
        (1,),
        (1, 0.5),
    ),
    # Aldehyde Oxidation, 2-step
    OperatorSmarts(
        "Aldehyde Oxidation, 2-step",
        "([C+0:1](=[O+0:2])[O+0H:3].[C+0:5](=[O+0:6])[O+0H:4])>>([*:1]=[*:2].[*:5]=[*:6]).[*:3]=[*:4]",
        (1,),
        (1, 1),
        number_of_steps=2,
    ),
    # Aldehyde & Alcohol Oxidation
    OperatorSmarts(
        "Aldehyde & Alcohol Oxidation, 2-step",
        "([C+0:1](=[O+0:2])[O+0H:3].[C+0:5](=[O+0:6])[O+0H]).[O+0H2:4]>>([*:1]=[*:2].[*:5][*:6]).[*:3]=[*:4]",
        (1, 1),
        (1, 1.5),
        number_of_steps=2,
    ),
    # Ketone Oxidation
    OperatorSmarts(
        "Ketone Oxidation",
        "[C,c;+0:1][C+0:2](=[O+0:3])[O+0H:6].[C,c;+0:5][C+0:4](=[O+0:7])[O+0H]>>[*:1][*:2](=[*:3])[*:4][*:5].[*:6]=[*:7]",
        (1, 1),
        (1, 1.5),
    ),
    OperatorSmarts(
        "Ketone Oxidation, Intramolecular",
        "([C,c;+0:1][C+0:2](=[O+0:3])[O+0H:6].[C,c;+0:5][C+0:4](=[O+0:7])[O+0H])>>[*:1][*:2](=[*:3])[*:4][*:5].[*:6]=[*:7]",
        (1,),
        (1, 1.5),
    ),
    # Baeyer-Villiger Oxidation (ketones and aldehydes)
    OperatorSmarts(
        "Baeyer-Villiger Oxidation (Ketones)",
        "[C,c;+0:5][C+0:1](=[O+0:2])[O+0:4][C,c;+0:3]>>[*:5][*:1](=[*:2])[*:3].[*:4]=[O]",
        (1,),
        (1, 0.5),
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Baeyer-Villiger Oxidation (Aldehydes)",  # with aldehydes doi.org/10.1002/0471264180.or043.03
        "[C+0H:1](=[O+0:2])[O+0:4][C$(*(C)(C)C),C$(*=*),C$(*c),c;+0:3]>>[*:1](=[*:2])[*:3].[*:4]=[O]",
        (1,),
        (1, 0.5),
    ),
    # Hydrogenation of Ketones      also works with CO2
    OperatorSmarts(
        "Hydrogenation of Ketones",
        "[C+0!H0!$(*(O)O)!$(*(O)(O)O):1][O+0H:2]>>[*:1]=[*:2].[H][H]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Hydrogenolysis ?
    # Keto-enol Tautomerization
    OperatorSmarts(
        "Keto-enol Tautomerization",
        "[C,N;+0:1]=[C+0:2][O,N;+0!H0:3]>>[*:1][*:2]=[*:3]",
        (1,),
        (1,),
        kekulize_flag=True,
    ),  # Tautomerism Cyclohexadienone
    OperatorSmarts(
        "Keto-enol Tautomerization Reverse",
        "[C,N;+0!H0:1][C+0:2]=[O,N;+0:3]>>[*:1]=[*:2][*:3]",
        (1,),
        (1,),
        kekulize_flag=True,
    ),
    # Decarbonylation of Aldehydes
    OperatorSmarts(
        "Decarbonylation of Aldehydes",
        "[C,c;+0!H0:1].[C-]#[O+]>>[*:1][C]=[O]",
        (1, 1),
        (1,),
    ),
    # Ketonization
    OperatorSmarts(
        "Ketonization",
        "[*;!O;+0:1][C+0:2](=[O+0:3])-!@[*;!O;+0:5].[O+0:4]=[C+0:6]=[O+0:7].[O+0H2:8]>>[*:1][*:2](=[*:3])[*:4].[*:5][*:6](=[*:7])[*:8]",
        (1, 1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Ketonization, Intramolecular",
        "[*;!O;+0:1][C+0:2](=[O+0:3])-@[*;!O;+0:5].[O+0:4]=[C+0:6]=[O+0:7].[O+0H2:8]>>([*:1][*:2](=[*:3])[*:4].[*:5][*:6](=[*:7])[*:8])",
        (1, 1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Oxidative Esterification of Aldehydes and Alcohols
    OperatorSmarts(
        "Oxidative Esterification of Aldehydes and Alcohols",
        "[C+0;!$(*=O):5][O+0:1]!@[C+0:3]=[O+0:2].[O+0H2:4]>>[*:5][*:1].[*:2]=[*:3].[*:4]=[O]",
        (1, 1),
        (1, 1, 0.5),
    ),
    OperatorSmarts(
        "Oxidative Esterification of Aldehydes and Alcohols, Intramolecular",
        "[C+0;!$(*=O):5][O+0:1]@[C+0:3]=[O+0:2].[O+0H2:4]>>([*:5][*:1].[*:2]=[*:3]).[*:4]=[O]",
        (1, 1),
        (1, 0.5),
        kekulize_flag=True,
    ),
    # McMurry Reaction
    OperatorSmarts(
        "McMurry Reaction",
        "[*+0:1][C+0;!$(*-O):2]=!@[C+0;!$(*-O):6][*+0:5].[O+0H2:3].[O+0H2:7]>>[*:1][*:2](=[*:3]).[*:5][*:6](=[*:7]).[H][H]",
        (1, 1, 1),
        (1, 1, 2),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "McMurry Reaction, Intramolecular",
        "[*+0:1][C+0;!$(*-O):2]=@[C+0;!$(*-O):6][*+0:5].[O+0H2:3].[O+0H2:7]>>([*:1][*:2](=[*:3]).[*:5][*:6](=[*:7])).[H][H]",
        (1, 1, 1),
        (1, 2),
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    # Hydration of Ketone and Aldehyde
    OperatorSmarts(
        "Hydration of Ketone and Aldehyde",
        "[C+0;!$(*-OC);!$(*(O)(O)(O));!$(*=O):2]([O+0H:3])[O+0H:4]>>[*:2]=[*:3].[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Hemiacetal Dissociation and Formation, Addition of Alcohols to Carbonyl Groups
    OperatorSmarts(
        "Hemiacetal Dissociation, Addition of Alcohols to Carbonyl Groups Reverse",
        "[CX3;!$(*O):1]=[O+0:2].[O+0H:3][C;!$(*=O):4]>>[*:1]([*:2])[*:3][*:4]",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Hemiacetal Dissociation, Addition of Alcohols to Carbonyl Groups Reverse, Intramolecular",
        "([C;!$(*O):1]=[O+0:2].[O+0H:3][C;!$(*=O):4])>>[*:1]([*:2])[*:3][*:4]",
        (1,),
        (1,),
    ),  # could use Retro_Not_Aromatic = True but ngthermo doesn't support *C=C=O anyway
    OperatorSmarts(
        "Hemiacetal Formation, Addition of Alcohols to Carbonyl Groups",
        "[C;!$(*=O):1]([O+0H:2])!@[O+0:3][C;!$(*=O):4]>>[*:1]=[*:2].[*:3][*:4]",
        (1,),
        (1, 1),
    ),
    OperatorSmarts(
        "Hemiacetal Formation, Addition of Alcohols to Carbonyl Groups, Intramolecular",
        "[C;!$(*=O):1]([O+0H:2])@[O+0:3][C;!$(*=O):4]>>([*:1]=[*:2].[*:3][*:4])",
        (1,),
        (1,),
    ),  # could use kekulize_flag = True for furan but ngthermo doesn't support *C=C=O anyway
    # Reduction of Carbonyl Groups
    OperatorSmarts(
        "Reduction of Carbonyl Groups",
        "[C,c,N;+0:1][C;H2,H3;+0:2].[O+0H2:3]>>[*:1][*:2]=[*:3].[H][H]",
        (1, 1),
        (1, 2),
        Retro_Not_Aromatic=True,
    ),
    # a-Halogenation
    OperatorSmarts(
        "a-Halogenation",
        "[C+0:2](=[O+0:3])[C+0:4][F,Cl,Br,I;+0:5].[F,Cl,Br,I;+0H:6]>>[*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
    ),
    # Wittig Reaction (Combined with Ylide Formation)
    # !NOT BALANCED! Reagents and by-products ignored for simplicity sake, needs to add a correction term for enthalpy calculation
    # Enthalpy correction from DFT: Ph3P + BuLi -> Ph3P=O + Bu + LiBr, delta H = -141.69 kcal/mol, gas phase 298.15 K
    OperatorSmarts(
        "Wittig Reaction (Combined with Ylide Formation)",
        "[C+0;!$(*~[O,S,N]):1]=!@[C+0X3;!$(*-O):4]>>[*:1][Br].[*:4]=[O]",
        (1,),
        (1, 1),
        enthalpy_correction=-141.69,  # DFT by QE
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Wittig Reaction, Intramolecular (Combined with Ylide Formation)",
        "[C+0;!$(*~[O,S,N]):1]=@[C+0;!$(*-O):4][C,c;+0:3]>>([*:1][Br].[*:3][*:4]=[O])",
        (1,),
        (1,),
        enthalpy_correction=-141.69,  # DFT by QE
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    # Knoevenagel Condensation
    # Synthesis of Enol Ethers from Aldehyde and Alcohol
    OperatorSmarts(
        "Synthesis of Enol Ethers from Aldehyde and Alcohol",
        "[CX4+0;H2,H3:1][O+0:2]-!@[C+0H:4]=[CX3+0:3].[O+0H2:5]>>[*:1][*:2].[*:3][*:4]=[*:5]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Synthesis of Enol Ethers from Aldehyde and Alcohol, Intramolecular",
        "[CX4+0;H2,H3:1][O+0:2]-@[C+0H:4]=[CX3+0:3].[O+0H2:5]>>([*:1][*:2].[*:3][*:4]=[*:5])",
        (1, 1),
        (1,),
    ),
    # Pinacol Coupling
    OperatorSmarts(
        "Pinacol Coupling",
        "[C+0X4;!$(*(-O)-O):2](-[O+0H:3])-!@[C+0X4;!$(*(-O)-O):6]-[O+0H:7]>>[*:2](=[*:3]).[*:6](=[*:7]).[H][H]",
        (1,),
        (1, 1, 1),
    ),
    OperatorSmarts(
        "Pinacol Coupling, Intramolecular",
        "[C+0X4;!$(*(-O)-O):2](-[O+0H:3])-@[C+0X4;!$(*(-O)-O):6]-[O+0H:7]>>([*:2](=[*:3]).[*:6](=[*:7])).[H][H]",
        (1,),
        (1, 1),
    ),
    # Carboxylic Acids ####################################################
    # Carboxylic Acids Decarboxylation
    OperatorSmarts(
        "Carboxylic Acids Decarboxylation",
        "[C,c;+0!H0:1].[O+0:3]=[C+0:2]=[O+0:4]>>[*:1][*:2](=[*:3])[*:4]",
        (1, 1),
        (1,),
    ),
    # Acid Anhydrides React with Alcohols to Form Esters
    OperatorSmarts(
        "Acid Anhydrides React with Alcohols to Form Esters",
        "[C+0;!$(*[OH]):1](=[O+0:2])[O+0!R:3][C,c;+0;!$(*=O):6].[C+0;!$(*([OH])[OH]):4](=[O+0:5])[O+0H:7]>>[*:1](=[*:2])[*:3][C*:4](=[*:5]).[*:6][*:7]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Acid Anhydrides React with Alcohols to Form Esters, Intramolecular",
        "([C+0;!$(*[OH]):1](=[O+0:2])[O+0!R:3][C;+0;!$(*=O):6].[C+0;!$(*([OH])[OH]):4](=[O+0:5])[O+0H:7])>>[*:1](=[*:2])[*:3][C*:4](=[*:5]).[*:6][*:7]",
        (1,),
        (1, 1),
        ring_issue=True,
    ),  # removed aromatic c:6 to avoid issue for things like O=C(Br)Oc1coc(C(=O)O)c1
    # Oxidation of Butane
    OperatorSmarts(
        "Oxidation of Butane",
        "[C+0]1(=[O+0])[C+0H]=[C+0H][C+0](=[O+0])[O+0]1.[O+0H2]>>[C][C][C][C].[O]=[O]",
        (1, 4),
        (1, 3.5),
    ),
    # Enols and Enolates ##################################################
    # Aldol Condensation
    OperatorSmarts(
        "Aldol Condensation",
        "[C!$(*[OH])+0:2](=[O+0:3])[C+0:4]-!@[C!$(*([OH])[OH])+0X4:6]([O+0H:5])>>[*:2](=[*:3])[*:4].[*:5]=[*:6]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Aldol Condensation, Intramolecular",
        "[C!$(*[OH])+0:2](=[O+0:3])[C+0:4]-@[C!$(*([OH])[OH])+0X4:6]([O+0H:5])>>([*:2](=[*:3])[*:4].[*:5]=[*:6])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Aldol Condensation (2H)",
        "[C!$(*[OH])+0:2](=[O+0:3])[C+0:4]=!@[C!$(*[OH])+0X3:6].[O+0H2:5]>>[*:2](=[*:3])[*:4].[*:5]=[*:6]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Aldol Condensation (2H), Intramolecular",
        "[C!$(*[OH])+0:2](=[O+0:3])[C+0:4]=@[C!$(*[OH])+0X3:6].[O+0H2:5]>>([*:2](=[*:3])[*:4].[*:5]=[*:6])",
        (1, 1),
        (1,),
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    # Claisen Condensation (including crossed)
    OperatorSmarts(
        "Claisen Condensation",
        "[C!$(*[OH])+0:2](=[O+0:3])-!@[C+0:8][C!$(*[OH])+0:6]=[O+0:5].[O+0H:7][C+0:4]>>[*:2](=[*:3])[*:7][*:4].[*:5]=[*:6][*:8]",
        (1, 1),
        (1, 1),
    ),
    # retro-Claisen condensation
    # Dieckmann Condensation (intramolecular version of Claisen Condensation)
    OperatorSmarts(
        "Dieckmann Condensation",
        "[C!$(*[OH])+0:2](=[O+0:3])-@[C+0:8][C!$(*[OH])+0:6]=[O+0:5].[O+0H:7][C+0:4]>>([*:2](=[*:3])[*:7][*:4].[*:5]=[*:6][*:8])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Michael Reaction
    OperatorSmarts(
        "Michael Reaction",
        "[C+0:1](=[O+0:2])[C+0:3](-!@[C+0:6][C+0!H0:7][C+0:8]=[O+0:9])[C+0:4]=[O+0:5]>>[*:1](=[*:2])[*:3][*:4]=[*:5].[*:6]=[*:7][C+0:8]=[O+0:9]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Michael Reaction, Intramolecular",
        "[C+0:1](=[O+0:2])[C+0:3](-@[C+0:6][C+0!H0:7][C+0:8]=[O+0:9])[C+0:4]=[O+0:5]>>([*:1](=[*:2])[*:3][*:4]=[*:5].[*:6]=[*:7][C+0:8]=[O+0:9])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # with a 6-membered ring
    OperatorSmarts(
        "Michael Reaction with Cyclic Ketones",
        "[C+0:1]1(=[O+0:2])[C+0:3]([C+0:10][C+0:11][C+0:12][C+0:13]1)-!@[C+0:6][C+0!H0:7][C+0:8]=[O+0:9]>>[*:1]1(=[*:2])[*:3][*:10][*:11][*:12][*:13]1.[*:6]=[*:7][*:8]=[*:9]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Michael Reaction with Cyclic Ketones, Intramolecular",
        "[C+0:1]1(=[O+0:2])[C+0:3]([C+0:10][C+0:11][C+0:12][C+0:13]1)-@[C+0:6][C+0!H0:7][C+0:8]=[O+0:9]>>([*:1]1(=[*:2])[*:3][*:10][*:11][*:12][*:13]1.[*:6]=[*:7][*:8]=[*:9])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Robinson Annulation (Michael-aldol sequence)
    OperatorSmarts(
        "Robinson Annulation",
        "[C+0:1]12[C+0:3]([C+0:8][C+0!H0:9][C+0:10](=[O+0:11])[C+0:12]=2)[C+0:14][C+0:15][C+0:16][C+0:17]1.[O+0H2:2]>>[*:1]1(=[O+0:2])[*:3][*:14][*:15][*:16][*:17]1.[*:8]=[*:9][*:10](=[*:11])[*:12]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
        ring_issue=True,
    ),
    # Esters ##############################################################
    # Hydrolysis of Esters (Covered by hydrolysis of ethers)
    # Esterification, Acid Anhydride Formation
    OperatorSmarts(
        "Esterification, Acid Anhydride Formation",
        "[C+0:2](=[O+0:3])!@[O+0:6][C,c;+0:5].[O+0H2:4]>>[*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Esterification, Acid Anhydride Formation, Intramolecular",
        "[C+0:2](=[O+0:3])@[O+0:6][C,c;+0:5].[O+0H2:4]>>([*:2](=[*:3])[*:4].[*:5][*:6])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Esterification of Acid Halides
    OperatorSmarts(
        "Esterification of Acid Halides",
        "[C+0:1](=[O+0:2])!@[O+0:5][C,c;!$(*=O);+0:4].[F,Cl,Br,I;+0H:3]>>[*:1](=[*:2])[*:3].[*:4][*:5]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Esterification of Acid Halides, Intramolecular",
        "[C+0:1](=[O+0:2])@[O+0:5][C,c;!$(*=O);+0:4].[F,Cl,Br,I;+0H:3]>>([*:1](=[*:2])[*:3].[*:4][*:5])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Ester Reduction
    # To Aldehydes
    OperatorSmarts(
        "Ester Reduction to Aldehydes and Alcohols",
        "[O+0H:1].[C+0!H0:2]=[O+0:3]>>[*:1][*:2]=[*:3].[H][H]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Ester Reduction to Aldehydes and Alcohols, Intramolecular",
        "([O+0H:1].[C+0!H0:2]=[O+0:3])>>[*:1][*:2]=[*:3].[H][H]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # To Alcohols
    OperatorSmarts(
        "Ester Reduction to Alcohols",
        "[O+0H:1].[C+0;H2,H3:2][O+0H:3]>>[*:1][*:2]=[*:3].[H][H]",
        (1, 1),
        (1, 2),
    ),
    OperatorSmarts(
        "Ester Reduction to Alcohols, Intramolecular",
        "([*+0:4][O+0H:1].[C+0;H2,H3:2][O+0H:3])>>[*:4][*:1][*:2]=[*:3].[H][H]",
        (1,),
        (1, 2),
        Retro_Not_Aromatic=True,
    ),
    # Transesterification
    OperatorSmarts(
        "Transesterification",
        "[C+0:1](=[O+0:2])!@[O+0:3][*+0:4].[*+0:6][O+0H;!$(*-C=O):5]>>[*:1](=[*:2])[*:5][*:6].[*:4][*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Transesterification, Intramolecular",
        "[C+0:1](=[O+0:2])@[O+0:3][*+0:4].[*+0:6][O+0H;!$(*-C=O):5]>>([*:1](=[*:2])[*:5][*:6].[*:4][*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Ester Hydrogenation
    # Ketenes #############################################
    OperatorSmarts(
        "[2+2] Cycloaddition",
        "[C+0:1]1[C+0:2](=[O+0:3])[O,N;+0:5][C!$(*(-O)-O)+0:4]1>>[*:1]=[*:2]=[*:3].[*:4]=[*:5]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Benzene and Derivatives #############################################
    # Benzene Hydrogenation
    OperatorSmarts(
        "Benzene Hydrogenation",
        "[C+0!H0:1]1[C+0!H0:2][C+0!H0:3][C+0!H0:4][C+0!H0:5][C+0!H0:6]1>>[*:1]1=[*:2][*:3]=[*:4][*:5]=[*:6]1.[H][H]",
        (1,),
        (1, 3),
    ),
    # Benzene Partial Hydrogenation
    OperatorSmarts(
        "Benzene Partial Hydrogenation 1",
        "[C+0:1]1=[C+0:2][C+0:3]=[C+0:4][C+0!H0:5][C+0!H0:6]1>>[*:1]1=[*:2][*:3]=[*:4][*:5]=[*:6]1.[H][H]",
        (1,),
        (1, 1),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Benzene Partial Hydrogenation 2",
        "[C+0:1]1=[C+0:2][C+0!H0:3][C+0!H0:4][C+0!H0:5][C+0!H0:6]1>>[*:1]1=[*:2][*:3]=[*:4][*:5]=[*:6]1.[H][H]",
        (1,),
        (1, 2),
        kekulize_flag=True,
    ),
    # Kolbe Carboxylation
    OperatorSmarts(
        "Kolbe Carboxylation",
        "[c+0:1]1:[c+0:2]([O+0H:7]):[c+0:3]([C+0:9](=[O+0:8])[O+0H:10]):[c+0:4]:[c+0:5]:[c+0:6]:1>>[*:1]1:[*:2]([*:7]):[*:3]:[*:4]:[*:5]:[*:6]:1.[*:8]=[*:9]=[*:10]",
        (1,),
        (1, 1),
    ),
    # Phenols Oxidation to Quinones
    # 1
    OperatorSmarts(
        "Phenols Oxidation to Quinones 1",
        "[C+0;!$(*~O):1]1[C+0:2](=[O+0:7])[C+0;!$(*~O):3]=[C+0;!$(*~O):4][C+0:5](=[O+0:8])[C+0;!$(*~O):6]=1.[O+0H2:9]>>[*:1]1[*:2]([*:7])=[*:3][*:4]=[*:5][*:6]=1.[*:8]=[*:9]",
        (1, 1),
        (1, 1),
    ),
    # 2
    OperatorSmarts(
        "Phenols Oxidation to Quinones 2",
        "[C+0;!$(*~O):1]1[C+0:2](=[O+0:7])[C+0:3](=[O+0:8])[C+0;!$(*~O):4]=[C+0;!$(*~O):5]([*+0:10])[C+0;!$(*~O):6]=1.[O+0H2:9]>>[*:1]1[*:2]([*:7])=[*:3][*:4]=[*:5]([*:10])[*:6]=1.[*:8]=[*:9]",
        (1, 1),
        (1, 1),
    ),
    # 3 & reverse
    OperatorSmarts(
        "Phenols Oxidation to Quinones 3",
        "[C+0;!$(*~O):1]1[C+0:2](=[O+0:7])[C+0:3](=[O+0:8])[C+0;!$(*~O):4]=[C+0;!$(*~O):5][C+0;!$(*~O):6]=1.[O+0H2:9]>>[*:1]1:[*:2]([*:7]):[*:3]([*:8]):[*:4]:[*:5]:[*:6]:1.[*:9]=[O]",
        (1, 1),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Phenols Oxidation to Quinones 3 Reverse",
        "[c+0:1]1:[c+0:2]([O+0H:7]):[c+0:3]([O+0H:8]):[c+0:4]:[c+0:5]:[c+0:6]:1>>[*:1]1[*:2](=[*:7])[*:3](=[*:8])[*:4]=[*:5][*:6]=1.[H][H]",
        (1,),
        (1, 1),
    ),
    # 4 & reverse
    OperatorSmarts(
        "Phenols Oxidation to Quinones 4",
        "[C+0;!$(*~O):1]1[C+0:2](=[O+0:7])[C+0;!$(*~O):3]=[C+0;!$(*~O):4][C+0:5](=[O+0:8])[C+0;!$(*~O):6]=1.[O+0H2:9]>>[*:1]1:[*:2]([*:7]):[*:3]:[*:4]:[*:5]([*:8]):[*:6]:1.[*:9]=[O]",
        (1, 1),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Phenols Oxidation to Quinones 4 Reverse",
        "[c+0:1]1:[c+0:2]([O+0H:7]):[c+0:3]:[c+0:4]:[c+0:5]([O+0H:8]):[c+0:6]:1>>[*:1]1[*:2](=[*:7])[*:3]=[*:4][*:5](=[*:8])[*:6]=1.[H][H]",
        (1,),
        (1, 1),
    ),
    # Quinones Addition
    OperatorSmarts(
        "Quinones Addition",
        "[c+0:1]1:[c+0:2]([O+0H:7]):[c+0:3]:[c+0:4]([F,Cl,Br,I;+0:9]):[c+0:5]([O+0H:8]):[c+0:6]:1>>[*:1]1[*:2](=[*:7])[*:3]=[*:4][*:5](=[*:8])[*:6]=1.[*:9]",
        (1,),
        (1, 1),
    ),
    # Naphthalene Oxidation
    # with CrO3
    OperatorSmarts(
        "Naphthalene Oxidation with CrO3",
        "[C+0:1]1[C+0:2](=[O+0:7])[c+0:3](:[c+0:9]:[c+0:10]:[c+0:11]:[c+0:12]:2)[c+0:4]2[C+0:5](=[O])[C+0:6]=1.[O+0H2:8]>>[*:1]1:[*:2]:[*:3](:[*:9]:[*:10]:[*:11]:[*:12]:2):[*:4]2:[*:5]:[*:6]:1.[*:7]=[*:8]",
        (1, 1),
        (1, 1.5),
    ),
    # with V2O5 catalyst
    OperatorSmarts(
        "Naphthalene Oxidation with V2O5 Catalyst",
        "[c+0:1]1:[c+0:2]:[c+0:3]([C+0:9](=[O+0])[O+0H]):[c+0:4]([C+0:12](=[O+0])[O+0H]):[c+0:5]:[c+0:6]:1.[O+0:7]=[C+0:10]=[O+0].[O+0H2:8]>>[*:1]1:[*:2]:[*:3](:[*:9]:[*:10]:[c]:[*:12]:2):[*:4]2:[*:5]:[*:6]:1.[*:7]=[*:8]",
        (1, 2, 1),
        (1, 4.5),
    ),
    # Oxidation of Aromatic Alkanes
    # with -CH3
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ar-CH3",
        "[c+0:1][C+0:2](=[O+0:3])[O+0H].[O+0H2:4]>>[*:1][*:2].[*:3]=[*:4]",
        (1, 1),
        (1, 1.5),
    ),
    # with -CH2CH3
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ar-CH2CH3",
        "[c+0:1][C+0:2](=[O+0:4])[O+0H].[O+0]=[C+0:3]=[O+0].[O+0H2:5]>>[*:1][*:2][*:3].[*:4]=[*:5]",
        (1, 1, 2),
        (1, 2.5),
    ),
    # with -(CH3)CH3
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ar-(CH3)CH3",
        "[c+0:1][C+0:2](=[O+0:4])[O+0H].[O+0]=[C+0:3]=[O+0].[O+0H2:5]>>[*:1][*:2]([*:3])[C].[*:4]=[*:5]",
        (1, 2, 3),
        (1, 4.5),
    ),
    # with long chain
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ar-long_chain",
        "[c+0:1][C+0:2](=[O+0:5])[O+0H].[C+0!H3:4][C+0:3](=[O+0])[O+0H].[O+0H2:6]>>[*:1][*:2][*:3][*:4].[*:5]=[*:6]",
        (1, 1, 1),
        (1, 2.5),
    ),
    # Ring-opening
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ring-opening 1",
        "([c+0:1][C+0:2](=[O+0:4])[O+0H].[C+0:3](=[O+0])[O+0H]).[O+0H2:5]>>[*:1][*:2][*:3].[*:4]=[*:5]",
        (1, 1),
        (1, 2.5),
    ),
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ring-opening 2",
        "([c+0:1][C+0:2](=[O+0:4])[O+0H].[C+0:3](=[O+0:5])[O+0H])>>[*:1][*:2]=[*:3].[*:4]=[*:5]",
        (1,),
        (1, 2),
        Retro_Not_Aromatic=True,
    ),
    # with -OH https://www.chemistrysteps.com/reactions-at-the-benzylic-position/
    # with C=C https://chem.libretexts.org/Courses/Athabasca_University/Chemistry_350%3A_Organic_Chemistry_I/16%3A_Chemistry_of_Benzene-_Electrophilic_Aromatic_Substitution/16.09%3A_Oxidation_of_Aromatic_Compounds
    # may use filter for stoi and simplify these
    # Oxidation of Aromatic Alkanes, 2-step
    # with -CH3
    OperatorSmarts(
        "Oxidation of Aromatic Alkanes Ar-CH3, 2-step",
        "([c+0:1][C+0:2](=[O+0:3])[O+0H].[c+0:5][C+0:6](=[O+0])[O+0H]).[O+0H2:4]>>([*:1][*:2].[*:5][*:6]).[*:3]=[*:4]",
        (1, 2),
        (1, 3),
        number_of_steps=2,
    ),
    # Oxidation of Aldehyde & Aromatic Alkanes
    # with -CH3
    OperatorSmarts(
        "Oxidation of Aldehyde & Aromatic Alkanes, 2-step",
        "([C+0:1](=[O+0:2])[O+0H:3].[c+0:5][C+0:6](=[O+0])[O+0H]).[O+0H2:4]>>([*:1]=[*:2].[*:5][*:6]).[*:3]=[*:4]",
        (1, 1),
        (1, 2),
        number_of_steps=2,
    ),
    # Oxidation of Alcohol & Aromatic Alkanes
    # with -CH3
    OperatorSmarts(
        "Oxidation of Alcohol & Aromatic Alkanes, 2-step",
        "([C+0:1](=[O+0:2])[O+0H:3].[c+0:5][C+0:6](=[O+0])[O+0H]).[O+0H2:4]>>([*:1][*:2].[*:5][*:6]).[*:3]=[*:4]",
        (1, 2),
        (1, 2.5),
        number_of_steps=2,
    ),
    # Halogenation of Aromatic Alkanes
    OperatorSmarts(
        "Halogenation of Aromatic Alkanes",
        "[c+0:1][C+0:2][F,Cl,Br,I;+0:3].[F,Cl,Br,I;+0H:4]>>[*:1][*:2].[*:3][*:4]",
        (1, 1),
        (1, 1),
    ),
    # Electrophilic Aromatic Alkylation with Alkenes
    OperatorSmarts(
        "Electrophilic Aromatic Alkylation with Alkenes",
        "[c+0:1]-!@[C+0:2][C+0!H0:3]>>[*:1].[*:2]=[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Electrophilic Aromatic Alkylation with Alkenes, Intramolecular",
        "[c+0:1]-@[C+0:2][C+0!H0:3]>>([*:1].[*:2]=[*:3])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Electrophilic Aromatic Alkylation with Alcohols
    OperatorSmarts(
        "Electrophilic Aromatic Alkylation with Alcohols",
        "[c+0:1]-!@[C+0;!$(*=O):2].[O+0H2:3]>>[*:1].[*:2][*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Electrophilic Aromatic Alkylation with Alcohols, Intramolecular",
        "[c+0:1]-@[C+0;!$(*=O):2].[O+0H2:3]>>([*:1].[*:2][*:3])",
        (1, 1),
        (1,),
    ),  # may use kekulize_flag = True but need to rewrite it first
    # Furan Carboxylation
    OperatorSmarts(
        "Furan Carboxylation",
        "[o+0:1]1:[c+0:2]([C+0:9](=[O+0:8])[O+0H:10]):[c+0:3]:[c+0:4]:[c+0:5]:1>>[*:1]1:[*:2]:[*:3]:[*:4]:[*:5]:1.[*:8]=[*:9]=[*:10]",
        (1,),
        (1, 1),
    ),
    # Furan Carboxylation, 2-step
    OperatorSmarts(
        "Furan Carboxylation, 2-step",
        "[o+0:1]1:[c+0:2]([C+0:9](=[O+0:8])[O+0H:10]):[c+0:3]:[c+0:4]:[c+0:5]([C+0](=[O+0])[O+0H]):1>>[*:1]1:[*:2]:[*:3]:[*:4]:[*:5]:1.[*:8]=[*:9]=[*:10]",
        (1,),
        (1, 2),
        number_of_steps=2,
    ),
    # Tautomerism Cyclohexadienone?
    # Friedel-Crafts Hydroxyalkylation
    OperatorSmarts(
        "Friedel-Crafts Hydroxyalkylation",
        "[c+0:1]-!@[CX4!$(*(-O)-O)!$(*(-O)(-O)-O)+0:2][O+0H:3]>>[*:1].[*:2]=[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Friedel-Crafts Hydroxyalkylation, Intramolecular",
        "[c+0:1]-@[CX4!$(*(-O)-O)!$(*(-O)(-O)-O)+0:2][O+0H:3]>>([*:1].[*:2]=[*:3])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Friedel-Crafts Hydroxyalkylation(BPA Synthesis)",
        "[c+0:1]-!@[CX4!$(*-O)!$(*(-O)-O)+0:3]-!@[c+0:2].[O+0H2:4]>>[*:1].[*:2].[*:3]=[*:4]",
        (1, 1),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Hock Process
    OperatorSmarts(
        "Hock Process",
        "[c+0:1][O+0H:5].[C+0H3:3][C+0:2](=[O+0:6])[C+0H3:4]>>[*:1][*:2]([*:3])[*:4].[*:5]=[*:6]",
        (1, 1),
        (1, 1),
    ),
    # Dehydrogenation of Ethylbenzene    This special case was added because it's the main industrial route for styrene (dH = 28.5 kcal/mol)
    OperatorSmarts(
        "Dehydrogenation of Ethylbenzene",
        "[cH]1[cH][cH][cH][cH][c]1[CH]=[CH2].[H][H]>>[c]1[c][c][c][c][c]1[C][C]",
        (1, 1),
        (1,),
    ),
    # Carbonylation #######################################################
    # Hydroformylation
    OperatorSmarts(
        "Hydroformylation",
        "[C+0!H0:1][C+0:2][C+0H:3]=[O+0:4]>>[*:1]=[*:2].[*-1:3]#[*+1:4].[H][H]",
        (1,),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Alcohol carbonylation to carboxylic acid, Cativa process
    OperatorSmarts(
        "Cativa Process",
        "[C!$(*=O)+0:1][C+0:3](=[O+0:4])[O+0H:2]>>[*:1][*:2].[*-1:3]#[*+1:4]",
        (1,),
        (1, 1),
    ),
    # Oxidative Carbonylation, Intramolecular?
    OperatorSmarts(
        "Oxidative Carbonylation 1",
        "[C!$(*=O)+0:1][O+0:2]!@[C+0:3](=[O+0:4])[O+0:6][C!$(*=O)+0:5].[O+0H2:7]>>[*:1][*:2].[*:5][*:6].[*-1:3]#[*+1:4].[*:7]=[O]",
        (1, 1),
        (1, 1, 1, 0.5),
    ),
    OperatorSmarts(
        "Oxidative Carbonylation 2",
        "[C!$(*=O)+0:1][O+0:2]!@[C+0:3](=[O+0:4])[C+0](=[O+0])[O+0:6][C!$(*=O)+0:5].[O+0H2:7]>>[*:1][*:2].[*:5][*:6].[*-1:3]#[*+1:4].[*:7]=[O]",
        (1, 1),
        (1, 1, 2, 0.5),
    ),
    # Hydrocarboxylation
    OperatorSmarts(
        "Hydrocarboxylation 1, Hydroesterification(Carboalkoxylation)",
        "[C+0!H0:1][C+0:2][C+0:3](=[O+0:4])-!@[O+0;!$(*(C=O)C=O):5]>>[*:1]=[*:2].[*-1:3]#[*+1:4].[*:5]",
        (1,),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Hydrocarboxylation 2",
        "[C+0!H0:1]=[C+0:2][C+0:3](=[O+0:4])[O+0H:5]>>[*:1]#[*:2].[*-1:3]#[*+1:4].[*:5]",
        (1,),
        (1, 1, 1),
    ),  # may use kekulize_flag = True but too rare
    # Hydrocarboxylation, 2-step
    OperatorSmarts(
        "Hydrocarboxylation, 2-step",
        "([C+0!H0:1][C+0:2][C+0:3](=[O+0:4])[O+0H:5].[C+0!H0:6][C+0:7][C+0](=[O+0])[O+0H])>>([*:1]=[*:2].[*:6]=[*:7]).[*-1:3]#[*+1:4].[*:5]",
        (1,),
        (1, 2, 2),
        Retro_Not_Aromatic=True,
        number_of_steps=2,
    ),
    # Tennessee Eastman Acetic Anhydride Process (similar to Cativa process)
    OperatorSmarts(
        "Tennessee Eastman Acetic Anhydride Process",
        "[C:1](=[O:2])[O:3][C:4](=[O:5])[C:6]>>[C+0:1](=[O+0:2])[O+0:3][C+0:6].[*-1:4]#[*+1:5]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Reppe Process
    OperatorSmarts(
        "Reppe Process",
        "[CX4+0!H0:1][CX4+0!H0:2][C+0H2][O+0H:3].[O]=[C]=[O]>>[*:1]=[*:2].[C-1]#[O+1].[*:3]",
        (1, 2),
        (1, 3, 2),
        Retro_Not_Aromatic=True,
    ),
    # Carbohydrates #######################################################
    # Oxidation of Pyranosides
    OperatorSmarts(
        "Oxidation of Pyranosides",
        "([C+0:9][C+0H:1]=[O+0:2].[C+0:10][C+0H:5]=[O+0:6]).[O+0H:7][C+0H:3]=[O+0:4].[O+0H2:8]>>[*:9][*:1]([*:2])[*:3]([*:4])[*:5]([*:6])[*:10].[*:7]=[*:8]",
        (1, 1, 1),
        (1, 1),
    ),
    # Lipids ##############################################################
    # Alkane Dehydrogenation by FAD (Fatty Acid Degradation)
    #    OperatorSmarts("Alkane Dehydrogenation by FAD (Fatty Acid Degradation)",
    #                   "[C+0:1]=[C+0:2].[O+0H2:3]>>[*:1][*:2].[*:3]=[O]",
    #                   (1, 1),(1, 0.5)),
    # Amines, Amides ##############################################################
    # Dehydration of Amides to Form Nitriles
    OperatorSmarts(
        "Dehydration of Amides",
        "[C+0:1]#[N+0:3].[O+0H2:2]>>[*:1](=[*:2])[*:3]",
        (1, 1),
        (1,),
    ),
    # ketone reductive amination
    OperatorSmarts(
        "Ketone Reductive Amination",
        "[CX4!$(*[O,S])!$(*(N)N)!$(*(N)(N)N)!H0+0:2]-!@[N+0X3:6].[O+0H2:3]>>[*:2]=[*:3].[*:6].[H][H]",
        (1, 1),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Ketone Reductive Amination, Intramolecular",
        "[CX4!$(*[O,S])!$(*(N)N)!$(*(N)(N)N)!H0+0:2]-@[N+0X3:6].[O+0H2:3]>>([*:2]=[*:3].[*:6]).[H][H]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Alkylation or Acylation of Amines
    OperatorSmarts(
        "Alkylation or Acylation of Amines",
        "[C,c;+0:1]-!@[NX3,n;+0:3].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Alkylation or Acylation of Amines, Intramolecular",
        "[C+0:1]-@[NX3+0:3].[F,Cl,Br,I;+0H:2]>>([*:1][*:2].[*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Alkylation of Tertiary Amines                             # generates ions, careful
    OperatorSmarts(
        "Alkylation of Tertiary Amines",
        "[C,c;+0:1]-!@[NX4H0+1:3].[F,Cl,Br,I;-1:2]>>[*:1][*+0:2].[*+0:3]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Amine Alkylation with Alcohols or Primary Amines
    OperatorSmarts(
        "Amine Alkylation with Alcohols or Primary Amines",
        "[C,c;!$(*=O)+0:1]-!@[NX3,n;+0:3].[OH2,NH3;+0:2]>>[*:1][*:2].[*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Amine Alkylation with Alcohols or Primary Amines, Intramolecular",
        "[C!$(*=O)+0:1]-@[NX3+0:3].[OH2,NH3;+0:2]>>([*:1][*:2].[*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Synthesis of Amides with Carboxylic Acid
    OperatorSmarts(
        "Synthesis of Amides with Carboxylic Acid",
        "[CX3!$(*[OH,SH])+0:2](=[O+0:3])-!@[N+0X3:5].[O+0H2:4]>>[*:2](=[*:3])[*:4].[*:5]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Synthesis of Amides with Carboxylic Acid, Intramolecular",
        "[CX3!$(*[OH,SH])+0:2](=[O+0:3])-@[N+0X3:5].[O+0H2:4]>>([*:2](=[*:3])[*:4].[*:5])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Synthesis of Amides with Acid Anhydrides or Esters
    OperatorSmarts(
        "Synthesis of Amides with Acid Anhydrides or Esters",
        "[C+0:2](=[O+0:3])-!@[N+0X3:5].[O+0H:4][C,c;+0:6]>>[*:2](=[*:3])[*:4][*:6].[*:5]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Synthesis of Amides with Acid Anhydrides or Esters, Intramolecular",
        "[C+0:2](=[O+0:3])-@[N+0X3:5].[O+0H:4][C,c;+0:6]>>([*:2](=[*:3])[*:4][*:6].[*:5])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Hydrolysis of Amides
    OperatorSmarts(
        "Hydrolysis of Amides",
        "[CX3+0:2](=[O+0:3])[O+0H:4].[N+0X3!H0:5]>>[*:2](=[*:3])[*:5].[*:4]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Hydrolysis of Amides, Intramolecular",
        "([CX3+0:2](=[O+0:3])[O+0H:4].[N+0X3!H0:5])>>[*:2](=[*:3])[*:5].[*:4]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Hofmann Elimination
    OperatorSmarts(
        "Hofmann Elimination R-NH2",  # can not garantee N has 3 identical side chains, so limit to N(CH3)(CH3)CH3
        "[C+0:1]=[C+0:2].[N+0:3]([C+0H3:4])([C+0H3])[C+0H3].[F,Cl,Br,I;+0H:5]>>[*:1][*:2][*:3].[*:4][*:5]",
        (1, 1, 3),
        (1, 3),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hofmann Elimination R-NHR",  # similar problem as above, so limit to N(CH3)(CH3)R
        "[C+0:1]=[C+0:2].[N+0:3]([C+0:4])([C+0H3])[C+0H3].[F,Cl,Br,I;+0H:5]>>[*:1][*:2][*:3][*:4].[C][*:5]",
        (1, 1, 2),
        (1, 2),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hofmann Elimination R-NHR Ringopening",  # similar problem as above
        "([C+0:1]=[C+0:2].[N+0:3]([C+0:4])([C+0H3])[C+0H3]).[F,Cl,Br,I;+0H:5]>>[*:1][*:2][*:3][*:4].[C][*:5]",
        (1, 2),
        (1, 2),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hofmann Elimination R-NRR",
        "[C+0:1]=[C+0:2].[N+0:3]([C+0:4])([C+0:6])!@[C+0:7].[F,Cl,Br,I;+0H:5]>>[*:1][*:2][*:3]([*:4])[*:6].[*:7][*:5]",
        (1, 1, 1),
        (1, 1),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hofmann Elimination R-NRR Ringopening",
        "([C+0:1]=[C+0:2].[N+0:3]([C+0:4])([C+0:6])-!@[C+0:7]).[F,Cl,Br,I;+0H:5]>>[*:1][*:2][*:3]([*:6])[*:4].[*:7][*:5]",
        (1, 1),
        (1, 1),
        kekulize_flag=True,
        ring_issue=True,
    ),
    # Hofmann Rearrangement
    OperatorSmarts(
        "Hofmann Rearrangement",
        "[C,c;+0:1][N+0H2:5].[O+0:3]=[C+0:2]=[O+0:4].[F,Cl,Br,I;+0H:6]>>[*:1][*:2](=[*:3])[*:5].[*:6][*:6].[*:4]",
        (1, 1, 2),
        (1, 1, 1),
    ),
    OperatorSmarts(
        "Hofmann Rearrangement with Alcohols",
        "[C,c;+0:1][N+0H:5][C+0:2](=[O+0:3])-!@[O+0:4][C+0!$(*=[O,S]):7].[F,Cl,Br,I;+0H:6]>>[*:1][*:2](=[*:3])[*:5].[*:6][*:6].[*:7][*:4]",
        (1, 2),
        (1, 1, 1),
    ),
    # Hydroamination of Alkenes
    OperatorSmarts(
        "Hydroamination of Alkenes",
        "[C+0!H0:1][C+0:2]-!@[N+0X3:3]>>[*:1]=[*:2].[*:3]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Hydroamination of Alkenes, Intramolecular",
        "[C+0!H0:1][C+0:2]-@[N+0X3:3]>>([*:1]=[*:2].[*:3])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Hydroamination of Alkynes
    OperatorSmarts(
        "Hydroamination of Alkynes",
        "[C+0!H0:1]=[C+0:2]-!@[N+0X3:3]>>[*:1]#[*:2].[*:3]",
        (1,),
        (1, 1),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hydroamination of Alkynes, Intramolecular",
        "[C+0!H0:1]=[C+0:2]-@[N+0X3:3]>>([*:1]#[*:2].[*:3])",
        (1,),
        (1,),
        kekulize_flag=True,
    ),
    # Hydroamination of Dienes
    OperatorSmarts(
        "Hydroamination of Dienes",
        "[C+0!H0:1][C+0:2]=[C+0:3][C+0:4]-!@[N+0X3:5]>>[*:1]=[*:2][*:3]=[*:4].[*:5]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Hydroamination of Dienes, Intramolecular",
        "[C+0!H0:1][C+0:2]=[C+0:3][C+0:4]-@[N+0X3:5]>>([*:1]=[*:2][*:3]=[*:4].[*:5])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Ring Opening of Epoxides by Amines
    OperatorSmarts(
        "Ring Opening of Epoxides by Amines",
        "[N+0X3:4]-!@[C+0:1][C+0:2][O+0H:3]>>[*:1]1[*:2][*:3]1.[*:4]",
        (1,),
        (1, 1),
    ),
    # Aromatic Nitrosation
    OperatorSmarts(
        "Aromatic Nitrosation",
        "[OH,N$(*([#6])([#6])[#6]);+0:10][c+0:1]1:[c+0:2]:[c+0:3]:[c+0:4]([N+0:8]=[O+0:9]):[c+0:5]:[c+0:6]:1.[O+0H2:7]>>[*:10][*:1]1:[*:2]:[*:3]:[*:4]:[*:5]:[*:6]:1.[*:7][*:8]=[*:9]",
        (1, 1),
        (1, 1),
    ),
    # Secondary Amines with Nitrous Acid
    OperatorSmarts(
        "Secondary Amines with Nitrous Acid",
        "[*+0:1][N+0:2]([N+0:5]=[O+0:6])[*+0:3].[O+0H2:4]>>[*:1][*:2][*:3].[*:4][*:5]=[*:6]",
        (1, 1),
        (1, 1),
    ),
    # Primary Amines with Nitrous Acid to Alcohols         not including possible rearrangement
    OperatorSmarts(
        "Primary Amines with Nitrous Acid to Alcohols",
        "[C,c;+0:1][O+0H:3].[O+0H2:5].[N+0:2]#[N+0:4]>>[*:1][*:2].[*:3][*:4]=[*:5]",
        (1, 1, 1),
        (1, 1),
    ),
    # Primary Amines with Nitrous Acid to Halides
    OperatorSmarts(
        "Primary Amines with Nitrous Acid to Halides",
        "[C,c;+0:1][F,Cl,Br,I;+0:3].[O+0H2:6].[N+0:2]#[N+0:5]>>[*:1][*:2].[*:3].[O][*:5]=[*:6]",
        (1, 2, 1),
        (1, 1, 1),
    ),
    # Primary Amines with Nitrous Acid to Alkenes         not including possible rearrangement
    OperatorSmarts(
        "Primary Amines with Nitrous Acid to Alkenes",
        "[C+0:6]=[C+0:1].[O+0H2:5].[N+0:2]#[N+0:4]>>[*:6][*:1][*:2].[O][*:4]=[*:5]",
        (1, 2, 1),
        (1, 1),
        kekulize_flag=True,
    ),
    # Tiffeneau–Demjanov Rearrangement
    OperatorSmarts(
        "Tiffeneau–Demjanov Rearrangement",
        "[O+0:1]=[C+0:2]([C+0:3])[C+0:5][C+0:4].[O+0H2:8].[N+0:6]#[N+0:7]>>[*:1][*:2]([*:3])([*:4])[*:5][*:6].[O][*:7]=[*:8]",
        (1, 2, 1),
        (1, 1),
    ),
    # Sandmeyer Cyanation
    OperatorSmarts(
        "Sandmeyer Cyanation",
        "[c+0:1][C+0:3]#[N+0:4].[O+0H2:6].[N+0:2]#[N+0:5]>>[*:1][*:2].[*:3]#[*:4].[O][*:5]=[*:6]",
        (1, 2, 1),
        (1, 1, 1),
    ),
    # Reduction of Primary Aromatic Amines
    OperatorSmarts(
        "Reduction of Primary Aromatic Amines",
        "[c+0H:1].[O+0H2:4].[N+0:2]#[N+0:3]>>[*:1][*:2].[H][H].[O][*:3]=[*:4]",
        (1, 2, 1),
        (1, 1, 1),
    ),
    # Cope Elimination
    OperatorSmarts(
        "Cope Elimination",
        "[C+0:1]=[C+0:2].[O+0H:6][N+0:3]([C+0:4])[C+0:5]>>[*:1][*:2][*:3]([*:4])[*:5].[O]=[*:6]",
        (1, 1),
        (1, 0.5),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Cope Elimination, Intramolecular",
        "([C+0:1]=[C+0:2].[O+0H:6][N+0:3]([C+0:4])[C+0:5])>>[*:1][*:2][*:3]([*:4])[*:5].[O]=[*:6]",
        (1,),
        (1, 0.5),
        kekulize_flag=True,
    ),
    # Hemiaminal Formation
    OperatorSmarts(
        "Hemiaminal Formation",
        "[CX4!$(*(O)O)+0:1]([O+0H:2])-!@[N,n;+0X3:3]>>[*:1]=[*:2].[*:3]",
        (1,),
        (1, 1),
        kekulize_flag=True,
    ),  # need to kekulize or could have kekulize error, don't know why
    OperatorSmarts(
        "Hemiaminal Formation, Reverse",
        "[CX3!$(*O)+0:1]=[O+0:2].[N,n;+0X3!H0:3]>>[*:1]([*:2])[*:3]",
        (1, 1),
        (1,),
    ),
    # Hemiaminal Dehydration
    OperatorSmarts(
        "Hemiaminal Dehydration",
        "[C+0:1]=[N+0:3].[O+0H2:2]>>[*:1]([*:2])[*:3]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Hemiaminal Dehydration, Reverse",
        "[C+0:1]([O+0H:2])[N+0X3!H0:3]>>[*:1]=[*:3].[*:2]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Nitroso, Nitro Compounds ###############################################
    # Reduction of Nitroso
    OperatorSmarts(
        "Reduction of Nitroso",
        "[C,c;+0:1][N+0H2:2].[O+0H2:3]>>[*:1][*:2]=[*:3].[H][H]",
        (1, 1),
        (1, 2),
    ),
    # Reduction of Nitro Compounds       will the charge in product cause problem in later generation?
    OperatorSmarts(
        "Reduction of Nitro Compounds",
        "[C,c;+0:1][NH2+0].[O+0H2:3]>>[*:1][N+1](=[*:3])[O-1].[H][H]",
        (1, 2),
        (1, 3),
    ),
    # Henry Reaction
    OperatorSmarts(
        "Henry Reaction",
        "[O+0H:6][CX4!$(*([OH])([OH])[OH])+0:5]-!@[C+0:1][N+1:2](=[O+0:3])[OX1-1:4]>>[*:1][*:2](=[*:3])[*:4].[*:5]=[*:6]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Henry Reaction, Intramolecular",
        "[O+0H:6][CX4!$(*([OH])([OH])[OH])+0:5]-@[C+0:1][N+1:2](=[O+0:3])[OX1-1:4]>>([*:1][*:2](=[*:3])[*:4].[*:5]=[*:6])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Benzene Nitration
    OperatorSmarts(
        "Benzene Nitration",
        "[c+0:1][N+1:3](=[O+0:4])[OX1-1:5].[O+0H2:2]>>[*:1].[*:2][*:3](=[*:4])[*:5]",
        (1, 1),
        (1, 1),
    ),
    # Oxidation of Nitroso
    OperatorSmarts(
        "Oxidation of Nitroso",
        "[*:1][N+1](=[O])[OX1-1]>>[*+0:1][N]=[O].[O]=[O]",
        (1,),
        (1, 0.5),
    ),
    # Esterification, Acid Anhydride Formation with Nitric Acid, Nitrate Esters Hydrolysis
    OperatorSmarts(
        "Esterification, Acid Anhydride Formation with Nitric Acid",
        "[C,c;+0:1][O+0:2][N+1:4](=[O+0:5])[OX1-1:6].[O+0H2:3]>>[*:1][*:2].[*:3][*:4](=[*:5])[*:6]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Nitrate Esters Hydrolysis",
        "[C,c;+0:1][O+0H:2].[O+0H:3][N+1:4](=[O+0:5])[OX1-1:6]>>[*:1][*:2][*:4](=[*:5])[*:6].[*:3]",
        (1, 1),
        (1, 1),
    ),
    # Nitrogen Dioxide Disproportionation
    OperatorSmarts(
        "Nitrogen Dioxide Disproportionation",
        "[O-1][N+1](=[O])[OH].[OH][N+0]=[O]>>[O-1][N+1]=[O].[O]",
        (1, 1),
        (2, 1),
    ),
    # Benzene Nitration, 2-step
    OperatorSmarts(
        "Benzene Nitration, 2-step",
        "[c!$(*aN)+0:1]([N+1:3](=[O+0:4])[OX1-1:5])[c+0:6][c!$(*aN)+0:7][N+1](=[O+0])[OX1-1].[O+0H2:2]>>[*:1]:[*:6]:[*:7].[*:2][*:3](=[*:4])[*:5]",
        (1, 2),
        (1, 2),
        number_of_steps=2,
    ),
    # Reduction of Nitro Compounds, 2-step
    OperatorSmarts(
        "Reduction of Nitro Compounds, 2-step",
        "([C,c;+0:1][NH2+0].[C,c;+0:2][NH2+0]).[O+0H2:3]>>([*:1][N+1](=[*:3])[O-1].[*:2][N+1](=[O])[O-1]).[H][H]",
        (1, 4),
        (1, 6),
        number_of_steps=2,
    ),
    # Hydrogenation of Nitric Oxide
    OperatorSmarts(
        "Hydrogenation of Nitric Oxide",
        "[N+0H2][O+0H]>>[NH0]=[O].[H][H]",
        (1,),
        (1, 1.5),
    ),
    # Imines ###############################################
    # Imines from Aldehydes and Ketones
    OperatorSmarts(
        "Imines from Aldehydes and Ketones",
        "[CX3!$(*[OH])+0:1]=!@[N+0:3].[O+0H2:2]>>[*:1]=[*:2].[*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Imines from Aldehydes and Ketones, Intramolecular",
        "[CX3!$(*[OH])+0:1]=@[N+0:3].[O+0H2:2]>>([*:1]=[*:2].[*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Imines from Aldehydes and Ketones Reverse",
        "[CX3!$(*[OH])+0:1]=[O+0:2].[N+0X3;H2,H3:3]>>[*:1]=[*:3].[*:2]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Imines from Aldehydes and Ketones, Intramolecular Reverse",
        "([CX3!$(*[OH])+0:1]=[O+0:2].[N+0X3;H2,H3:3])>>[*:1]=[*:3].[*:2]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Treatment of Aldehydes and Ketones with a Secondary Amine
    OperatorSmarts(
        "Treatment of Aldehydes and Ketones with a Secondary Amine",
        "[C,N;+0:4]=[CX3!$(*[OH])+0:1]-!@[NX3+0:3].[O+0H2:2]>>[*:4][*:1]=[*:2].[*:3]",
        (1, 1),
        (1, 1),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Treatment of Aldehydes and Ketones with a Secondary Amine, Intramolecular",
        "[C,N;+0:4]=[CX3!$(*[OH])+0:1]-@[NX3+0:3].[O+0H2:2]>>([*:4][*:1]=[*:2].[*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Treatment of Aldehydes and Ketones with a Secondary Amine Reverse",
        "[C,N;+0!H0:4][CX3!$(*[OH])+0:1]=[O+0:2].[N+0X3H:3]>>[*:4]=[*:1][*:3].[*:2]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Treatment of Aldehydes and Ketones with a Secondary Amine, Intramolecular Reverse",
        "([C,N;+0!H0:4][CX3!$(*[OH])+0:1]=[O+0:2].[N+0X3H:3])>>[*:4]=[*:1][*:3].[*:2]",
        (1,),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Oxime-Nitroso Tautomerization
    OperatorSmarts(
        "Oxime-Nitroso Tautomerization",
        "[C+0!H0:1][N+0:2]=[O+0:3]>>[*:1]=[*:2][*:3]",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Oxime-Nitroso Tautomerization Reverse",
        "[C+0:1]=[N+0:2][O+0H:3]>>[*:1][*:2]=[*:3]",
        (1,),
        (1,),
        kekulize_flag=True,
    ),
    # Reduction of Imines
    OperatorSmarts(
        "Reduction of Imines",
        "[C+0!H0:1][N+0!H0:2]>>[*:1]=[*:2].[H][H]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Beckmann Rearrangement
    OperatorSmarts(
        "Beckmann Rearrangement with Ketoximes",
        "[C,c;+0:1][C+0:2](=[O+0:4])[N+0H:3][C,c;+0:5]>>[*:1][*:2](=[*:3][*:4])[*:5]",
        (1,),
        (1,),
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Beckmann Rearrangement with Aldoximes",
        "[C,c;+0:1][C+0:2]#[N+0:3].[O+0H2:4]>>[*:1][*:2]=[*:3][*:4]",
        (1, 1),
        (1,),
    ),
    # Beckmann Rearrangement from Ketones and Aldehydes
    OperatorSmarts(
        "Beckmann Rearrangement from Ketones",
        "[C,c;+0:1][C+0:2](=[O+0:3])[N+0H:5][C,c;+0:4].[O+0H2:6]>>[*:1][*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
        kekulize_flag=True,
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Beckmann Rearrangement from Aldehydes",
        "[C,c;+0:1][C+0:2]#[N+0:4].[O+0H2:3]>>[*:1][*:2]=[*:3].[*:4][O]",
        (1, 2),
        (1, 1),
    ),
    # Beckmann Fragmentation              note: here only consider tertiary carbocations since they're more stable
    OperatorSmarts(
        "Beckmann Fragmentation",
        "[C,c;+0:1][C+0:2]#[N+0:3].[C+0:5]([C+0:6])([C+0:7])=[*+0:8].[O+0H2:4]>>[*:1][*:2](=[*:3][*:4])[*:5]([*:6])([*:7])[*:8]",
        (1, 1, 1),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Beckmann Fragmentation, Intramolecular",
        "([C,c;+0:1][C+0:2]#[N+0:3].[C+0:5]([C+0:6])([C+0:7])=[*+0:8]).[O+0H2:4]>>[*:1][*:2](=[*:3][*:4])[*:5]([*:6])([*:7])[*:8]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Semmler–Wolff Reaction
    OperatorSmarts(
        "Semmler–Wolff Reaction",
        "[C+0:1]1[C+0:2]=[C+0:3][C+0:4]=[C+0:5][C+0:6]=1[N+0H2:7].[O+0H2:8]>>[*:1]1[*:2][*:3][*:4]=[*:5][*:6]1=[*:7][*:8]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Transimination
    OperatorSmarts(
        "Transimination",
        "[C,c;+0:1]=!@[N!$(*[O,S])+0:2].[N!$(*[O,S]);H2,H3;+0:3]>>[*:1]=[*:3].[*:2]",
        (1, 1),
        (1, 1),
    ),
    # Imine Metathesis
    OperatorSmarts(
        "Imine Metathesis",
        "[C,c;+0:1]=!@[N!$(*[O,S])+0:2].[C,c;+0:3]=!@[N!$(*[O,S])+0:4]>>[*:1]=[*:4].[*:3]=[*:2]",
        (1, 1),
        (1, 1),
    ),
    # Wolff–Kishner Reduction
    OperatorSmarts(
        "Wolff–Kishner Reduction",
        "[C,c;+0:1][C!$(*[O,S]);H2,H3;+0:2].[N+0:3]#[N+0:4]>>[*:1][*:2](=[*:3][*:4])",
        (1, 1),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Amino Acids, Nitriles ###############################################
    # Cyanation (Kolbe Nitrile Synthesis)
    OperatorSmarts(
        "Cyanation (Kolbe Nitrile Synthesis)",
        "[C,c+0:1][C+0:3]#[N+0:4].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]#[*:4]",
        (1, 1),
        (1, 1),
    ),
    # Cyanation of Ketones or Aldehydes (Cyanohydrin Reaction)
    OperatorSmarts(
        "Cyanation of Ketones or Aldehydes (Cyanohydrin Reaction)",
        "[CX4!$(*[S,N])!$(*(O)O)!$(*(O)(O)O)+0:1]([C+0:3]#[N+0:4])[O+0H:2]>>[*:1]=[*:2].[*:3]#[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Alkyl Cyanides from Haloalkanes
    OperatorSmarts(
        "Alkyl Cyanides from Haloalkanes",
        "[C+0:1][C+0:3]#[N+0:4].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]#[*:4]",
        (1, 1),
        (1, 1),
    ),
    # Nitrile Hydrogenation to Amines
    OperatorSmarts(
        "Nitrile Hydrogenation to Amines",
        "[C+0;H2,H3:1]-[N+0H2:2]>>[*:1]#[*:2].[H][H]",
        (1,),
        (1, 2),
    ),
    # Amines Dehydrogenation to Nitriles
    OperatorSmarts(
        "Amines Dehydrogenation to Nitriles",
        "[C+0:1]#[N+0:2].[H][H]>>[*:1][*:2]",
        (1, 2),
        (1,),
    ),
    # Amines Oxidative Dehydrogenation to Nitriles
    OperatorSmarts(
        "Amines Oxidative Dehydrogenation to Nitriles",
        "[C+0:1]#[N+0:2].[O+0H2:3]>>[*:1][*:2].[*:3]=[O]",
        (1, 2),
        (1, 1),
    ),
    # Nitrile Hydrogenation to Aldehydes
    OperatorSmarts(
        "Nitrile Hydrogenation to Aldehydes",
        "[C+0;H1,H2:1]=[O+0:3].[N+0H3:2]>>[*:1]#[*:2].[*:3].[H][H]",
        (1, 1),
        (1, 1, 1),
    ),
    # Nitrile Hydrogenation to Imines
    OperatorSmarts(
        "Nitrile Hydrogenation to Imines",
        "[C+0;H1,H2:1]=[N+0H:2]>>[*:1]#[*:2].[H][H]",
        (1,),
        (1, 1),
    ),
    # Nitrile Hydrogenation to Secondary Amines
    OperatorSmarts(
        "Nitrile Hydrogenation to Secondary Amines",
        "[C+0;H2,H3:1]!@[N+0H:2][C+0;H2,H3:3].[N+0H3:4]>>[*:1]#[*:2].[*:3]#[*:4].[H][H]",
        (1, 1),
        (1, 1, 4),
    ),
    OperatorSmarts(
        "Nitrile Hydrogenation to Secondary Amines, Intramolecular",
        "[C+0;H2:1]-@[N+0H:2][C+0;H2:3].[N+0H3:4]>>([*:1]#[*:2].[*:3]#[*:4]).[H][H]",
        (1, 1),
        (1, 4),
    ),
    # Nitrile Hydrogenation to Tertiary Amines
    OperatorSmarts(
        "Nitrile Hydrogenation to Tertiary Amines",
        "[C+0;H2,H3:1]!@[N+0:2](!@[C+0;H2,H3:3])!@[C+0;H2,H3:5].[N+0H3:4]>>[*:1]#[*:2].[*:3]#[*:4].[*:5]#[N].[H][H]",
        (1, 2),
        (1, 1, 1, 6),
    ),
    # Hydrolysis of Nitriles
    OperatorSmarts(
        "Hydrolysis of Nitriles",
        "[C+0:1](=[O+0])[O+0H:3].[N+0H3:2]>>[*:1]#[*:2].[*:3]",
        (1, 1),
        (1, 2),
    ),
    # Nitriles to Ketones with Grignard Reagents
    # !NOT BALANCED! Reagents and by-products ignored for simplicity sake, needs to add a correction term for enthalpy calculation
    # Enthalpy correction from DFT: Mg -> MgBrOH, delta H = -93.89 kcal/mol, gas phase 298.15 K
    OperatorSmarts(
        "Nitriles to Ketones with Grignard Reagents",
        "[C+0:1](=[O+0:4])-!@[c,C!$(*~O);!$(*#*);+0:3].[N+0H3:2]>>[*:1]#[*:2].[*:3][Br].[*:4]",
        (1, 1),
        (1, 1, 2),
        enthalpy_correction=-93.89,
    ),  # DFT by QE
    # Partial Hydrolysis of Nitriles
    OperatorSmarts(
        "Partial Hydrolysis of Nitriles",
        "[C+0:1](=[O+0:3])[N+0H2:2]>>[*:1]#[*:2].[*:3]",
        (1,),
        (1, 1),
    ),
    # Epoxides Ring Opening with Cyanides
    OperatorSmarts(
        "Epoxides Ring Opening with Cyanides",
        "[N+0:5]#[C+0:4][C+0:1][C+0:2][O+0H:3]>>[*:1]1[*:2][*:3]1.[*:4]#[*:5]",
        (1,),
        (1, 1),
    ),
    # Andrussow Process
    OperatorSmarts(
        "Andrussow Process",
        "[C+0H:1]#[N+0:2].[O+0H2:3]>>[*:1].[*:2].[*:3]=[O]",
        (2, 6),
        (2, 2, 3),
    ),
    # Hydrocyanation
    OperatorSmarts(
        "Hydrocyanation",
        "[C+0!H0:1][C+0:2][C+0:3]#[N+0:4]>>[*:1]=[*:2].[*:3]#[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Hydrocyanation, 2-step
    OperatorSmarts(
        "Hydrocyanation, 2-step",
        "([C+0!H0:1][C+0:2][C+0:5]#[N+0:6].[C+0!H0:3][C+0:4][C+0]#[N+0])>>([*:1]=[*:2].[*:3]=[*:4]).[*:5]#[*:6]",
        (1,),
        (1, 2),
        Retro_Not_Aromatic=True,
        number_of_steps=2,
    ),
    # Ammoxidation
    OperatorSmarts(
        "Ammoxidation",
        "[C+0:1]=[C+0:2][C+0:3]#[N+0:5].[O+0H2:4]>>[*:1]=[*:2][*:3].[*:4]=[O].[*:5]",
        (1, 3),
        (1, 1.5, 1),
        kekulize_flag=True,
    ),
    # Bucherer–Bergs Reaction
    OperatorSmarts(
        "Bucherer–Bergs Reaction",
        "[CX4!$(*-[O])+0:1]1[C+0:3](=[O+0:2])[N+0H:4][C+0:7](=[O+0:6])[N+0H:5]1.[O+0H2:8]>>[*:1]=[*:2].[*:3]#[*:4].[*:5].[*:6]=[*:7]=[*:8]",
        (1, 1),
        (1, 1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Azides ###############################################
    # Azide-Alkyne, Azide-Nitrile Cycloaddition                   will charge in product cause problems?
    OperatorSmarts(
        "Azide-Alkyne, Azide-Nitrile Cycloaddition",
        "[N+0:1]1[N+0]=[N+0][C,N;+0:4]=[C+0:5]1>>[*:1]=[N+1]=[N-1].[*:4]#[*:5]",
        (1,),
        (1, 1),
        ring_issue=True,
        kekulize_flag=True,
    ),
    # Azide Salts as Nucleophiles
    OperatorSmarts(
        "Azide Salts as Nucleophiles",  # works with carboxylic acid
        "[C+0:1][N+0:3]=[N+1:4]=[N-1:5].[FH,ClH,BrH,IH,OH2;+0:2]>>[*:1][*:2].[*:3]=[*:4]=[*:5]",
        (1, 1),
        (1, 1),
    ),
    # Reduction of Azides
    OperatorSmarts(
        "Reduction of Azides",
        "[NX3+0H2:1].[N]#[N]>>[*:1]=[N+1]=[N-1].[H][H]",
        (1, 1),
        (1, 1),
    ),
    # Curtius Rearrangement
    OperatorSmarts(
        "Curtius Rearrangement",
        "[C,c;+0:1][N+0:4]=[C+0:2]=[O+0:3].[N]#[N]>>[*:1][*:2](=[*:3])[*:4]=[N+1]=[N-1]",
        (1, 1),
        (1,),
    ),
    # Diazo ###############################################
    # Esters from Diazoes and Carboxylic Acids                    will charge in product cause problems?
    OperatorSmarts(
        "Esters from Diazoes and Carboxylic Acids",
        "[CX3!$(*[OH])+0:1](=[O+0:2])[O+0:3]-!@[CX4+0!H0:4].[N]#[N]>>[*:1](=[*:2])[*:3].[*:4]=[N+1]=[N-1]",
        (1, 1),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Isocyanates, Isothiocyanate ###############################################
    # Isocyanates, Isothiocyanate with Nucleophiles
    OperatorSmarts(
        "Isocyanates, Isothiocyanate with Nucleophiles",
        "[C,c;+0:1][N+0H:2][C+0:3](=[O,S;+0:4])-!@[NX3,O;+0:5]>>[*:1][*:2]=[*:3]=[*:4].[*:5]",
        (1,),
        (1, 1),
    ),
    # Isocyanates with Water
    OperatorSmarts(
        "Isocyanates with Water",
        "[C,c;+0:1][N+0H2:2].[C+0:3](=[O+0:4])=[O+0:5]>>[*:1][*:2]=[*:3]=[*:4].[*:5]",
        (1, 1),
        (1, 1),
    ),
    # Isocyanates with Carboxylic Acid
    OperatorSmarts(
        "Isocyanates with Carboxylic Acid",
        "[C,c;+0:1][N+0H:2][C+0:3](=[O+0:4])-!@[C,c;+0:8].[O+0:5]=[C+0:6]=[O+0:7]>>[*:1][*:2]=[*:3]=[*:4].[*:5][*:6](=[*:7])[*:8]",
        (1, 1),
        (1, 1),
    ),
    # Synthesis of Isocyanates, Isothiocyanates
    OperatorSmarts(
        "Synthesis of Isocyanates, Isothiocyanates",
        "[C,c;+0:1][N+0:2]=[C+0:4]=[O,SX1;+0:5].[Cl+0H:6]>>[*:1][*:2].[Cl][*:4](=[*:5])[*:6]",
        (1, 2),
        (1, 1),
    ),
    OperatorSmarts(
        "Synthesis of Isocyanates, Isothiocyanates, 2-step",
        "([C,c;+0:1][N+0:2]=[C+0:4]=[O,SX1;+0:5].[C,c;+0:7][N+0:8]=[C+0]=[O,SX1;+0]).[Cl+0H:6]>>([*:1][*:2].[*:7][*:8]).[Cl][*:4](=[*:5])[*:6]",
        (1, 4),
        (1, 2),
        number_of_steps=2,
    ),
    # Synthesis of Isothiocyanates
    OperatorSmarts(
        "Synthesis of Isothiocyanates",
        "[C,c;+0:1][N+0:2]=[C+0:4]=[S+0:5].[SX2+0H2:3]>>[*:1][*:2].[*:3]=[*:4]=[*:5]",
        (1, 1),
        (1, 1),
    ),
    # Thiols, Thioethers ###############################################
    # Hydrosulfide Anion Substitution with Alkyl Halides
    OperatorSmarts(
        "Hydrosulfide Anion Substitution with Alkyl Halides",
        "[C,c;+0:1]-!@[SX2+0:3].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Hydrosulfide Anion Substitution with Alkyl Halides, Intramolecular",
        "[C,c;+0:1]-@[SX2+0:3].[F,Cl,Br,I;+0H:2]>>([*:1][*:2].[*:3])",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Preparation of Sulfides
    OperatorSmarts(
        "Preparation of Sulfides",
        "[C,c;+0:1]-!@[SX2+0:5][C,c;+0:3].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3][*:2].[*:5]",
        (1, 2),
        (1, 1, 1),
    ),
    OperatorSmarts(
        "Preparation of Sulfides, Intramolecular",
        "[C,c;+0:1]-@[SX2+0:5][C,c;+0:3].[F,Cl,Br,I;+0H:2]>>([*:1][*:2].[*:3][*:2]).[*:5]",
        (1, 2),
        (1, 1),
        kekulize_flag=True,
    ),
    # Thiols from Thiourea
    OperatorSmarts(
        "Thiols from Thiourea",
        "[C,c;+0:1][SX2+0H:3].[O+0:7]=[C+0:4]([N+0H2:5])[N+0H2:6].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]=[*:4]([*:5])[*:6].[*:7]",
        (1, 1, 1),
        (1, 1, 1),
    ),
    # Thioacetals from Thiols and Aldehydes or Ketones
    OperatorSmarts(
        "Thioacetals from Thiols and Aldehydes or Ketones",
        "[C,c;+0:1][SX2+0:2]-!@[C!$(*O)X4+0:5]-!@[SX2+0:4][C,c;+0:3].[O+0H2:6]>>[*:1][*:2].[*:3][*:4].[*:5]=[*:6]",
        (1, 1),
        (1, 1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Cyclic Thioacetals from Dithiols
    OperatorSmarts(
        "Cyclic Thioacetals from Dithiols",
        "[C,c;+0:1]-@[SX2+0:2][C!$(*O)X4+0:5][SX2+0:4]-@[C,c;+0:3].[O+0H2:6]>>([*:1][*:2].[*:3][*:4]).[*:5]=[*:6]",
        (1, 1),
        (1, 1),
        ring_issue=True,
        Retro_Not_Aromatic=True,
    ),
    # Oxidation of Thiols, Reduction of Disulfides
    OperatorSmarts(
        "Oxidation of Thiols",
        "[C,c;+0:1][SX2+0:2]-!@[SX2+0:4][C,c;+0:3].[O+0H2:5]>>[*:1][*:2].[*:3][*:4].[*:5]=[O]",
        (1, 1),
        (1, 1, 0.5),
    ),
    OperatorSmarts(
        "Oxidation of Thiols, Intramolecular",
        "[C,c;+0:1][SX2+0:2]-@[SX2+0:4][C,c;+0:3].[O+0H2:5]>>([*:1][*:2].[*:3][*:4]).[*:5]=[O]",
        (1, 1),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Reduction of Disulfides",
        "[C,c;+0:1][SX2+0H:2].[C,c;+0:3][SX2+0H:4]>>[*:1][*:2][*:4][*:3].[H][H]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Reduction of Disulfides, Intramolecular",
        "([C,c;+0:1][SX2+0H:2].[C,c;+0:3][SX2+0H:4])>>[*:1][*:2][*:4][*:3].[H][H]",
        (1,),
        (1, 1),
    ),
    # Thiol-ene Reaction
    OperatorSmarts(
        "Thiol-ene Reaction",
        "[C,c;+0:1][SX2+0:2]-!@[C+0:3][C+0!H0:4]>>[*:1][*:2].[*:3]=[*:4]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Thiol-ene Reaction, Intramolecular",
        "[C,c;+0:1][SX2+0:2]-@[C+0:3][C+0!H0:4]>>([*:1][*:2].[*:3]=[*:4])",
        (1,),
        (1,),
        Retro_Not_Aromatic=True,
    ),
    # Sulfides Hydrogenolysis
    OperatorSmarts(
        "Sulfides Hydrogenolysis",
        "[C,c;+0!H0:1].[C,c;+0!H0:3].[SX2+0H2:2]>>[*:1][*:2][*:3].[H][H]",
        (1, 1, 1),
        (1, 2),
    ),
    OperatorSmarts(
        "Sulfides Hydrogenolysis, Intramolecular",  # works for aromatic ring
        "([C,c;+0!H0:1].[C,c;+0!H0:3]).[SX2+0H2:2]>>[*:1][*:2][*:3].[H][H]",
        (1, 1),
        (1, 2),
    ),
    # Oxidation of Disulfides
    OperatorSmarts(
        "Oxidation of Disulfides",
        "[C,c;+0:1][SX4+0:2](=[O+0:5])(=[O+0:6])[O+0H:7].[C,c;+0:4][SX4+0:3](=[O+0])(=[O+0])[O+0H]>>[*:1][*:2][*:3][*:4].[*:5]=[*:6].[*:7]",
        (1, 1),
        (1, 2.5, 1),
    ),
    OperatorSmarts(
        "Oxidation of Disulfides, Intramolecular",
        "([C,c;+0:1][SX4+0:2](=[O+0:5])(=[O+0:6])[O+0H:7].[C,c;+0:4][SX4+0:3](=[O+0])(=[O+0])[O+0H])>>[*:1][*:2][*:3][*:4].[*:5]=[*:6].[*:7]",
        (1,),
        (1, 2.5, 1),
    ),
    # Cleavage of Disulfides by Halogens
    OperatorSmarts(
        "Cleavage of Disulfides by Halogens",
        "[C,c;+0:1][SX2+0:2][F,Cl,Br,I;+0:5].[C,c;+0:4][SX2+0:3][F,Cl,Br,I;+0:6]>>[*:1][*:2][*:3][*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Cleavage of Disulfides by Halogens, Intramolecular",
        "([C,c;+0:1][SX2+0:2][F,Cl,Br,I;+0:5].[C,c;+0:4][SX2+0:3][F,Cl,Br,I;+0:6])>>[*:1][*:2][*:3][*:4].[*:5][*:6]",
        (1,),
        (1, 1),
    ),
    # Sulfoxides ###############################################
    # Oxidation of Sulfides, Sulfoxides
    OperatorSmarts(
        "Oxidation of Sulfides",  # works for S1C=CC=C1, retro aromatic ok
        "[*+0:1][SX3!$(*[OH])+0:2](=[O+0:4])[*+0:3]>>[*:1][*:2][*:3].[*:4]=[O]",
        (1,),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Oxidation of Sulfoxides",
        "[*+0:1][SX4+0:2](=[O+0:4])(=[O+0:5])[*+0:3]>>[*:1][*:2](=[*:4])[*:3].[*:5]=[O]",
        (1,),
        (1, 0.5),
    ),
    # Deoxygenation of Sulfoxides
    OperatorSmarts(
        "Deoxygenation of Sulfoxides",
        "[C,c;+0:1][SX2+0:2][C,c;+0:3].[O+0H2:4]>>[*:1][*:2](=[*:4])[*:3].[H][H]",
        (1, 1),
        (1, 1),
        kekulize_flag=True,
    ),
    # Thermal Elimination of Sulfoxides
    OperatorSmarts(
        "Thermal Elimination of Sulfoxides",
        "[C,c;+0:1][SX2+0:2][O+0H:3].[C+0:4]=[C+0:5]>>[*:1][*:2](=[*:3])[*:4][*:5]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Thiones ###############################################
    # Thione-Thiol Tautomerization
    OperatorSmarts(
        "Thione-Thiol Tautomerization",
        "[N,O;+0:1]=[C+0:2][SX2+0H:3]>>[*:1][*:2]=[*:3]",
        (1,),
        (1,),
        kekulize_flag=True,
    ),
    OperatorSmarts(
        "Thione-Thiol Tautomerization Reverse",
        "[N,O;+0!H0:1][C+0:2]=[SX1+0:3]>>[*:1]=[*:2][*:3]",
        (1,),
        (1,),
        kekulize_flag=True,
    ),
    # Sulfenic, Sulfinic, Sulfonic, Sulfuric Acids ###############################################
    # Sulfenic Acid Tautomerization
    OperatorSmarts(
        "Sulfenic Acid Tautomerization",
        "[C,c;+0:1][SX3+0H:2]=[O+0:3]>>[*:1][*:2][*:3]",
        (1,),
        (1,),
    ),
    # Sulfenic Acid Tautomerization
    OperatorSmarts(
        "Sulfenic Acid Tautomerization Reverse",
        "[C,c;+0:1][SX2+0:2][O+0H:3]>>[*:1][*:2]=[*:3]",
        (1,),
        (1,),
    ),
    # Thiol Oxidation to Sulfenic Acid, Sulfinic Acid, Sulfonic Acid
    OperatorSmarts(
        "Thiol Oxidation to Sulfenic Acid",
        "[C,c;+0:1][SX2+0:2][O+0H:3]>>[*:1][*:2].[*:3]=[O]",
        (1,),
        (1, 0.5),
    ),
    OperatorSmarts(
        "Thiol Oxidation to Sulfinic Acid",
        "[C,c;!$(*=O)+0:1][SX3+0:2](=[O+0:3])[O+0H:4]>>[*:1][*:2].[*:3]=[*:4]",
        (1,),
        (1, 1),
    ),
    OperatorSmarts(
        "Thiol Oxidation to Sulfonic Acid",
        "[C,c;!$(*=O)+0:1][SX4+0:2](=[O+0:3])(=[O+0])[O+0H:4]>>[*:1][*:2].[*:3]=[*:4]",
        (1,),
        (1, 1.5),
    ),
    # Sulfurous Acid Salts Addition to Oxiranes
    OperatorSmarts(
        "Sulfurous Acid Salts Addition to Oxiranes",
        "[O+0H:2][CX4+0:1][CX4+0:3][SX4+0:5](=[O+0:4])(=[O+0:6])[O+0H:7]>>[*:1]1[*:2][*:3]1.[*:4]=[*:5]([*:6])[*:7]",
        (1,),
        (1, 1),
    ),
    # Sulfuric Acid Esterification, Acid Anhydride Formation, Organosulfates Hydrolysis
    OperatorSmarts(
        "Sulfuric Acid Esterification, Acid Anhydride Formation",
        "[C,c;+0:1][O+0:2]-!@[SX4+0:4](=[O+0:3])(=[O+0:5])[OX2+0:6].[O+0H2:7]>>[*:1][*:2].[*:3]=[*:4](=[*:5])([*:6])[*:7]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Organosulfates Hydrolysis",
        "[C,c;+0:1][O+0H:2].[O+0:3]=[SX4+0:4](=[O+0:5])([OX2+0:6])[O+0H:7]>>[*:1][*:2][*:4](=[*:3])(=[*:5])[*:6].[*:7]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Sulfuric Acid Esterification, Acid Anhydride Formation, Intramolecular",
        "[C,c;+0:1][O+0:2]-@[SX4+0:4](=[O+0:3])(=[O+0:5])[OX2+0:6].[O+0H2:7]>>([*:1][*:2].[*:3]=[*:4](=[*:5])([*:6])[*:7])",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Organosulfates Hydrolysis, Intramolecular",
        "([C,c;+0:1][O+0H:2].[O+0:3]=[SX4+0:4](=[O+0:5])([OX2+0:6])[O+0H:7])>>[*:1][*:2][*:4](=[*:3])(=[*:5])[*:6].[*:7]",
        (1,),
        (1, 1),
    ),
    # Organosulfates Reduction
    OperatorSmarts(
        "Organosulfates Reduction",
        "[C!$(*=O)+0:1][SX4+0:3](=[O+0:4])(=[O+0:5])[O+0H:6].[O+0H2:2]>>[*:1][*:2][*:3](=[*:4])(=[*:5])[*:6].[H][H]",
        (1, 1),
        (1, 1),
    ),
    # Alkenes Addition by Sulfuric Acid
    OperatorSmarts(
        "Alkenes Addition by Sulfuric Acid",
        "[C+0!H0:1][C+0:2][O+0:6][SX4+0:4](=[O+0:3])(=[O+0:5])[O+0H:7]>>[*:1]=[*:2].[*:3]=[*:4](=[*:5])([*:6])[*:7]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    OperatorSmarts(
        "Alkenes Addition by Sulfuric Acid Reverse",
        "[C+0:1]=[C+0:2].[O+0:3]=[SX4+0:4](=[O+0:5])([O+0H:6])[O+0H:7]>>[*:1][*:2][*:6][*:4](=[*:3])(=[*:5])[*:7]",
        (1, 1),
        (1,),
        kekulize_flag=True,
    ),
    # Alkenes Addition by Bisulfites
    OperatorSmarts(
        "Alkenes Addition by Bisulfites",
        "[C+0!H0:1][C+0:2][SX4+0:4](=[O+0:3])(=[O+0:5])[O+0H:6]>>[*:1]=[*:2].[*:3]=[*:4]([*:5])[*:6]",
        (1,),
        (1, 1),
        Retro_Not_Aromatic=True,
    ),
    # Esterification of Sulfonic Acids, Sulfonic Acid Esters Hydrolysis
    OperatorSmarts(
        "Esterification of Sulfonic Acids",
        "[C,c;+0:1][O+0:2]-!@[SX4+0:4](=[O+0:3])(=[O+0:5])[C,c,N;+0:6].[OH2,FH,ClH,BrH,IH;+0:7]>>[*:1][*:2].[*:3]=[*:4](=[*:5])([*:6])[*:7]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Sulfonic Acid Esters Hydrolysis",
        "[C,c;+0:1][O+0H:2].[O+0:3]=[SX4+0:4](=[O+0:5])([C,c,N;+0:6])[OH+0:7]>>[*:1][*:2][*:4](=[*:3])(=[*:5])[*:6].[*:7]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Esterification of Sulfonic Acids, Intramolecular",
        "[C,c;+0:1][O+0:2]-@[SX4+0:4](=[O+0:3])(=[O+0:5])[C,c,N;+0:6].[OH2,FH,ClH,BrH,IH;+0:7]>>([*:1][*:2].[*:3]=[*:4](=[*:5])([*:6])[*:7])",
        (1, 1),
        (1,),
    ),
    OperatorSmarts(
        "Sulfonic Acid Esters Hydrolysis, Intramolecular",
        "([C,c;+0:1][O+0H:2].[O+0:3]=[SX4+0:4](=[O+0:5])([C,c,N;+0:6])[OH+0:7])>>[*:1][*:2][*:4](=[*:3])(=[*:5])[*:6].[*:7]",
        (1,),
        (1, 1),
    ),
    OperatorSmarts(
        "Sulfonic Esters Nucleophilic Substitution",
        "[C,c;+0:1][F,Cl,Br,I;+0:2].[O+0:3]=[SX4+0:4](=[O+0:5])([C,c;+0:6])[OH+0:7]>>[*:1][*:7][*:4](=[*:3])(=[*:5])[*:6].[*:2]",
        (1, 1),
        (1, 1),
    ),
    OperatorSmarts(
        "Sulfonic Esters Nucleophilic Substitution, Intramolecular",
        "([C,c;+0:1][F,Cl,Br,I;+0:2].[O+0:3]=[SX4+0:4](=[O+0:5])([C,c;+0:6])[OH+0:7])>>[*:1][*:7][*:4](=[*:3])(=[*:5])[*:6].[*:2]",
        (1,),
        (1, 1),
    ),
    # Sulfonation of Benzene
    OperatorSmarts(
        "Sulfonation of Benzene",
        "[c+0:1][SX4+0:3](=[O+0:4])(=[O+0:5])[O+0H:2]>>[*:1].[*:2]=[*:3](=[*:4])=[*:5]",
        (1,),
        (1, 1),
    ),
    # Disproportionation of Aromatic Sulfinic Acids
    # Can not make retro rule for this
    # Alkylation of Sulfinic Acids with Halides
    OperatorSmarts(
        "Alkylation of Sulfinic Acids with Halides",
        "[C,c;+0:1][SX4+0:2](=[O+0:3])(=[O+0:4])-!@[C,c;+0:5].[F,Cl,Br,I;+0H:6]>>[*:1][*:2](=[*:3])[*:4].[*:5][*:6]",
        (1, 1),
        (1, 1),
    ),
    # Reduction of Aromatic Sulfonyl Chlorides to Thiols
    OperatorSmarts(
        "Reduction of Aromatic Sulfonyl Chlorides to Thiols",
        "[c+0:1][SX2+0H:2].[F,Cl,Br,I;+0H:4].[O+0H2:3]>>[*:1][*:2](=[*:3])(=[O])[*:4].[H][H]",
        (1, 1, 2),
        (1, 3),
    ),
    # Reduction of Sulfonyl Chlorides to Sulfinic Acids
    OperatorSmarts(
        "Reduction of Sulfonyl Chlorides to Sulfinic Acids",
        "[C,c;+0:1][SX3+0:2](=[O+0:3])[O+0H:4].[F,Cl,Br,I;+0H:5]>>[*:1][*:2](=[*:3])(=[*:4])[*:5].[H][H]",
        (1, 1),
        (1, 1),
    ),
    # Strecker Sulfite Alkylation
    OperatorSmarts(
        "Strecker Sulfite Alkylation",
        "[C,c;+0:1][SX4+0:4](=[O+0:3])(=[O+0:5])[O+0H:6].[F,Cl,Br,I;+0H:2]>>[*:1][*:2].[*:3]=[*:4]([*:5])[*:6]",
        (1, 1),
        (1, 1),
    ),
    # Hydrolysis of Sulfonyl Halides
    OperatorSmarts(
        "Hydrolysis of Sulfonyl Halides",
        "[C,c;+0:1][SX4+0:2](=[O+0:3])(=[O+0:4])[O+0H:6].[F,Cl,Br,I;+0H:5]>>[*:1][*:2](=[*:3])(=[*:4])[*:5].[*:6]",
        (1, 1),
        (1, 1),
    ),
    # Reed Reaction
    OperatorSmarts(
        "Reed Reaction",
        "[C,c;+0:1][SX4+0:2](=[O+0:3])(=[O+0:4])[F,Cl,Br,I;+0:6].[F,Cl,Br,I;+0H:5]>>[*:1].[*:2](=[*:3])(=[*:4]).[*:5][*:6]",
        (1, 1),
        (1, 1, 1),
    ),
    # Sulfoxidation
    OperatorSmarts(
        "Sulfoxidation",
        "[C+0:1][SX4+0:2](=[O+0:3])(=[O+0:4])[O+0H:5]>>[*:1].[*:2](=[*:3])(=[*:4]).[*:5]=[O]",
        (1,),
        (1, 1, 0.5),
    ),
    # other Coupling reaction
)


# print(len(op_retro_smarts)+3)
