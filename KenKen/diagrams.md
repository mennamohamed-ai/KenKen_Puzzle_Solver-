# KenKen Solver - Block Diagrams & Flowcharts

## 1. Block Diagram - System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      KenKen Solver                            │
│                      (Main Application)                      │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │         GUI Layer (gui.py)           │
        │  ┌──────────────────────────────┐   │
        │  │   KenKenGUI Class            │   │
        │  │  - User Interface            │   │
        │  │  - Input Handling            │   │
        │  │  - Display Management        │   │
        │  │  - ScrollableFrame           │   │
        │  └──────────────────────────────┘   │
        └──────────────┬───────────────────────┘
                       │
        ┌──────────────┴───────────────┐
        │                              │
        ▼                              ▼
┌───────────────┐            ┌──────────────────┐
│  Grid Module  │            │  Solver Modules   │
│  (grid.py)    │            │                  │
│               │            │  ┌──────────────┐ │
│  KenKenGrid   │            │  │ Backtracking│ │
│  - Grid Data  │            │  │  Algorithm  │ │
│  - Cages      │            │  └──────────────┘ │
│  - Operations │            │                  │
└───────┬───────┘            │  ┌──────────────┐ │
        │                     │  │   Cultural   │ │
        │                     │  │  Algorithm   │ │
        │                     │  └──────────────┘ │
        │                     └──────────────────┘
        │                              │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │   Constraints Module          │
        │   (constraints.py)            │
        │  ┌────────────────────────┐  │
        │  │ - valid_in_row_col()    │  │
        │  │ - cage_valid_partial()  │  │
        │  │ - cage_satisfied()      │  │
        │  │ - check_all_constraints()│  │
        │  └────────────────────────┘  │
        └──────────────────────────────┘
```

## 2. Flowchart - Main Application Flow

```mermaid
flowchart TD
    Start([Start Application]) --> Init[Initialize GUI]
    Init --> Wait[Wait for User Input]
    
    Wait --> UserAction{User Action}
    
    UserAction -->|Set Grid Size| Reset[Reset Grid]
    UserAction -->|Add Cage| AddCage[Add Cage to Grid]
    UserAction -->|Solve| Solve[Select Algorithm]
    UserAction -->|Clear| Clear[Clear Cages]
    UserAction -->|Reset| Reset
    
    Reset --> DrawGrid[Draw Grid]
    DrawGrid --> UpdateDisplay[Update Display]
    UpdateDisplay --> Wait
    
    AddCage --> ValidateCage[Validate Cage Format]
    ValidateCage -->|Valid| AddToGrid[Add to Grid Object]
    ValidateCage -->|Invalid| ShowError[Show Error Message]
    AddToGrid --> UpdateColors[Update Cage Colors]
    UpdateColors --> DrawBorders[Draw Cage Borders]
    DrawBorders --> UpdateDisplay
    ShowError --> Wait
    
    Clear --> ClearGrid[Clear Grid Cages]
    ClearGrid --> UpdateDisplay
    
    Solve --> CheckCages{Cages Exist?}
    CheckCages -->|No| AskContinue[Ask to Continue]
    CheckCages -->|Yes| SelectAlgo[Select Algorithm]
    AskContinue -->|No| Wait
    AskContinue -->|Yes| SelectAlgo
    
    SelectAlgo --> AlgoType{Algorithm Type}
    AlgoType -->|Backtracking| RunBT[Run Backtracking]
    AlgoType -->|Cultural| RunCA[Run Cultural Algorithm]
    
    RunBT --> BTResult{Solution Found?}
    BTResult -->|Yes| DisplaySolution[Display Solution]
    BTResult -->|No| ShowError
    
    RunCA --> CAResult{Solution Found?}
    CAResult -->|Yes| DisplaySolution
    CAResult -->|No| ShowBest[Show Best Found]
    
    DisplaySolution --> ShowMetrics[Show Metrics]
    ShowBest --> ShowMetrics
    ShowMetrics --> Wait
    
    style Start fill:#90EE90
    style DisplaySolution fill:#90EE90
    style ShowError fill:#FFB6C1
```

## 3. Flowchart - Backtracking Algorithm

```mermaid
flowchart TD
    Start([Start Backtracking]) --> Init[Initialize Variables]
    Init --> BuildMap[Build cell_to_cage Map]
    BuildMap --> CallBT[Call backtrack Function]
    
    CallBT --> FindEmpty[Find Empty Cell]
    FindEmpty --> CheckEmpty{Empty Cell Found?}
    
    CheckEmpty -->|No| CheckComplete[Grid Complete]
    CheckComplete --> VerifyCages[Verify All Cages]
    VerifyCages --> AllValid{All Cages Valid?}
    AllValid -->|Yes| Success[Mark as Solved]
    AllValid -->|No| Fail[Return False]
    
    CheckEmpty -->|Yes| GetPos[Get Cell Position r,c]
    GetPos --> IncrementIter[Increment Iterations]
    IncrementIter --> TryValues[Try Values 1 to n]
    
    TryValues --> CheckValue{More Values?}
    CheckValue -->|No| Backtrack[Return False]
    
    CheckValue -->|Yes| GetVal[Get Next Value]
    GetVal --> CheckConstraints[Check All Constraints]
    
    CheckConstraints --> Valid{Value Valid?}
    Valid -->|No| TryValues
    Valid -->|Yes| PlaceValue[Place Value in Grid]
    
    PlaceValue --> RecursiveCall[Recursive Call backtrack]
    RecursiveCall --> RecResult{Result?}
    
    RecResult -->|Success & Enough Solutions| Success
    RecResult -->|Continue| RemoveValue[Remove Value Backtrack]
    RecResult -->|Failed| RemoveValue
    
    RemoveValue --> TryValues
    Backtrack --> Return[Return Result]
    Success --> Return
    Fail --> Return
    
    Return --> End([End])
    
    style Start fill:#90EE90
    style Success fill:#90EE90
    style Fail fill:#FFB6C1
    style Backtrack fill:#FFD700
```

## 4. Flowchart - Cultural Algorithm

```mermaid
flowchart TD
    Start([Start Cultural Algorithm]) --> Init[Initialize Population]
    Init --> InitBelief[Initialize Belief Matrix]
    InitBelief --> GenLoop[Generation Loop]
    
    GenLoop --> CheckTimeout{Timeout?}
    CheckTimeout -->|Yes| ReturnBest[Return Best Found]
    CheckTimeout -->|No| Evaluate[Evaluate Population]
    
    Evaluate --> CalculateFitness[Calculate Fitness for Each]
    CalculateFitness --> SortPop[Sort by Fitness]
    SortPop --> UpdateBest{Better than Best?}
    
    UpdateBest -->|Yes| SaveBest[Save as Best]
    UpdateBest -->|No| CheckSolved{Best Fitness = 0?}
    SaveBest --> CheckSolved
    
    CheckSolved -->|Yes| Success[Return Success]
    CheckSolved -->|No| SelectElites[Select Elites]
    
    SelectElites --> UpdateBelief[Update Belief Matrix]
    UpdateBelief --> NewPop[Create New Population]
    
    NewPop --> AddElites[Add Elites to New Population]
    AddElites --> PopLoop{Population Full?}
    
    PopLoop -->|No| Tournament[Tournament Selection]
    Tournament --> Crossover[Apply Crossover]
    Crossover --> Mutate[Apply Mutation]
    Mutate --> AddToPop[Add to Population]
    AddToPop --> PopLoop
    
    PopLoop -->|Yes| ReplacePop[Replace Old Population]
    ReplacePop --> NextGen[Next Generation]
    NextGen --> GenLoop
    
    Success --> End([End])
    ReturnBest --> End
    
    style Start fill:#90EE90
    style Success fill:#90EE90
    style ReturnBest fill:#FFD700
```

## 5. Flowchart - Constraint Checking

```mermaid
flowchart TD
    Start([Check Constraints for Cell]) --> CheckRow[Check Row Uniqueness]
    CheckRow --> RowValid{Value in Row?}
    
    RowValid -->|Yes| Invalid[Return False]
    RowValid -->|No| CheckCol[Check Column Uniqueness]
    
    CheckCol --> ColValid{Value in Column?}
    ColValid -->|Yes| Invalid
    ColValid -->|No| FindCage[Find Cage Containing Cell]
    
    FindCage --> BuildVals[Build Values List with New Value]
    BuildVals --> CheckPartial[Check cage_valid_partial]
    
    CheckPartial --> PartialValid{Partial Valid?}
    PartialValid -->|No| Invalid
    
    PartialValid -->|Yes| CheckFilled{All Cells Filled?}
    CheckFilled -->|No| Valid[Return True]
    
    CheckFilled -->|Yes| CheckSatisfied[Check cage_satisfied]
    CheckSatisfied --> SatisfiedValid{Satisfied?}
    
    SatisfiedValid -->|Yes| Valid
    SatisfiedValid -->|No| Invalid
    
    Valid --> End([End])
    Invalid --> End
    
    style Start fill:#90EE90
    style Valid fill:#90EE90
    style Invalid fill:#FFB6C1
```

## 6. Flowchart - Cage Validation (Partial)

```mermaid
flowchart TD
    Start([cage_valid_partial]) --> GetFilled[Get Filled Values]
    GetFilled --> CheckEmpty{Any Filled?}
    
    CheckEmpty -->|No| ReturnTrue[Return True - Conservative]
    CheckEmpty -->|Yes| CheckOp{Operation Type?}
    
    CheckOp -->|+| CheckSum[Check Sum]
    CheckOp -->|*| CheckProd[Check Product]
    CheckOp -->|-| CheckDiff[Check Difference]
    CheckOp -->|/| CheckDiv[Check Division]
    CheckOp -->|=| CheckEqual[Check Equality]
    
    CheckSum --> SumGT{Sum > Target?}
    SumGT -->|Yes| ReturnFalse[Return False]
    SumGT -->|No| SumEQ{Sum = Target?}
    SumEQ -->|Yes| AllFilled{All Cells Filled?}
    SumEQ -->|No| ReturnTrue
    
    AllFilled -->|No| ReturnFalse
    AllFilled -->|Yes| ReturnTrue
    
    CheckProd --> ProdGT{Product > Target?}
    ProdGT -->|Yes| ReturnFalse
    ProdGT -->|No| ProdEQ{Product = Target?}
    ProdEQ -->|Yes| AllFilled
    ProdEQ -->|No| ReturnTrue
    
    CheckDiff --> BothFilled{Both Cells Filled?}
    BothFilled -->|Yes| CheckAbsDiff[Check |a-b| = Target]
    BothFilled -->|No| ReturnTrue
    CheckAbsDiff -->|Yes| ReturnTrue
    CheckAbsDiff -->|No| ReturnFalse
    
    CheckDiv --> BothFilled2{Both Cells Filled?}
    BothFilled2 -->|Yes| CheckDivOp[Check a/b or b/a = Target]
    BothFilled2 -->|No| ReturnTrue
    CheckDivOp -->|Yes| ReturnTrue
    CheckDivOp -->|No| ReturnFalse
    
    CheckEqual --> ValEQ{Value = Target?}
    ValEQ -->|Yes| ReturnTrue
    ValEQ -->|No| ReturnFalse
    
    ReturnTrue --> End([End])
    ReturnFalse --> End
    
    style Start fill:#90EE90
    style ReturnTrue fill:#90EE90
    style ReturnFalse fill:#FFB6C1
```

## 7. Component Interaction Diagram

```
┌──────────────┐
│   User       │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│         GUI (KenKenGUI)             │
│                                     │
│  ┌────────────┐  ┌──────────────┐ │
│  │   Input    │  │   Display    │ │
│  │  Handler   │  │   Manager    │ │
│  └─────┬──────┘  └──────┬───────┘ │
│        │                │          │
│        │                │          │
│        ▼                ▼          │
│  ┌──────────────────────────────┐ │
│  │      Grid Operations          │ │
│  └──────────────┬───────────────┘ │
└──────────────────┼─────────────────┘
                   │
        ┌───────────┴───────────┐
        │                        │
        ▼                        ▼
┌──────────────┐      ┌──────────────────┐
│ KenKenGrid   │      │   Constraints    │
│              │      │                  │
│ - grid[][]   │◄─────┤ - Row/Col Check  │
│ - cages[]    │      │ - Cage Check     │
│              │      │ - Partial Valid  │
└──────┬───────┘      └──────────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│      Solver Selection              │
│                                     │
│  ┌──────────────┐  ┌────────────┐ │
│  │ Backtracking  │  │  Cultural  │ │
│  │               │  │            │ │
│  │ - Recursive   │  │ - Pop-based│ │
│  │ - Systematic  │  │ - Belief   │ │
│  └───────┬───────┘  └──────┬─────┘ │
│          │                 │       │
│          └────────┬────────┘       │
│                   │                │
│                   ▼                │
│          ┌─────────────────┐      │
│          │  Use Constraints │      │
│          └─────────────────┘      │
└─────────────────────────────────────┘
```

## 8. Data Flow Diagram

```
┌─────────────┐
│ User Input  │
│ - Grid Size │
│ - Cages     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  GUI Processing │
│  - Validate      │
│  - Store         │
└──────┬───────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  KenKenGrid     │──────┤  Constraints │
│  Data Structure │      │  Validator   │
│                 │      │              │
│  grid: int[][]  │      │  - Row/Col   │
│  cages: Cage[]  │      │  - Cage Rules │
└──────┬──────────┘      └──────────────┘
       │
       │
       ▼
┌─────────────────┐
│  Solver Engine  │
│                 │
│  ┌───────────┐ │
│  │ Backtrack  │ │
│  └─────┬─────┘ │
│        │       │
│  ┌─────▼─────┐ │
│  │ Cultural  │ │
│  └─────┬─────┘ │
└────────┼────────┘
         │
         ▼
┌─────────────────┐
│  Solution Grid  │
│  (Filled)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Display Result │
│  - Grid Values  │
│  - Metrics      │
└─────────────────┘
```

## 9. Class Diagram

```
┌─────────────────────┐
│    KenKenGUI        │
├─────────────────────┤
│ + root              │
│ + grid_obj          │
│ + cells[][]         │
│ + scrollable        │
├─────────────────────┤
│ + __init__()        │
│ + reset()           │
│ + add_cage()        │
│ + draw_grid()       │
│ + solve()           │
│ + update_cage_colors()│
└──────────┬──────────┘
           │ uses
           ▼
┌─────────────────────┐
│    KenKenGrid       │
├─────────────────────┤
│ + n: int            │
│ + grid: int[][]     │
│ + cages: Cage[]     │
├─────────────────────┤
│ + add_cage()        │
│ + get_cages()       │
│ + get_cell()        │
│ + set_cell()        │
└──────────┬──────────┘
           │ uses
           ▼
┌─────────────────────┐
│   Constraints       │
├─────────────────────┤
│ + valid_in_row_col()│
│ + cage_valid_partial()│
│ + cage_satisfied()   │
│ + check_all_constraints()│
└─────────────────────┘

┌─────────────────────┐
│  Backtracking       │
├─────────────────────┤
│ + solve_backtracking()│
│ - find_empty_cell() │
│ - backtrack()       │
└─────────────────────┘

┌─────────────────────┐
│ CulturalAlgorithm   │
├─────────────────────┤
│ + solve()           │
│ - fitness()         │
│ - update_belief()   │
│ - crossover()       │
│ - mutate()          │
└─────────────────────┘
```

## 10. Sequence Diagram - Solving Process

```
User    GUI      Grid      Constraints  Solver
 │       │        │            │          │
 │──Add──>│        │            │          │
 │       │──Add───>│            │          │
 │       │<───────│            │          │
 │       │        │            │          │
 │──Solve>│        │            │          │
 │       │        │            │          │
 │       │───────────Check─────>│          │
 │       │<──────────Valid──────│          │
 │       │        │            │          │
 │       │─────────────────────Solve─────>│
 │       │        │            │          │
 │       │        │<───Check───│          │
 │       │        │───Valid───>│          │
 │       │        │            │          │
 │       │<──────────────────Solution──────│
 │       │──Update──>│            │          │
 │<──Show──│        │            │          │
```

---

## Notes

- **Block Diagrams**: Show the overall system architecture and relationships between components
- **Flowcharts**: Illustrate the workflow for each algorithm and main process
- **Component Interaction**: Shows how components interact with each other
- **Data Flow**: Illustrates data flow from inputs to outputs
- **Class Diagram**: Shows the class structure and relationships between them
- **Sequence Diagram**: Shows the sequence of operations when solving the puzzle

