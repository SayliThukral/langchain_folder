from typing import TypedDict
from langgraph.graph import StateGraph, END

# -----------------------------
# Define State
# -----------------------------
class QuadState(TypedDict):
    a: float
    b: float
    c: float
    equation: str
    discriminant: float
    result: str


# -----------------------------
# Node 1: Show Equation
# -----------------------------
def show_equation(state: QuadState):
    equation = f"{state['a']}x^2 + {state['b']}x + {state['c']}"
    return {"equation": equation}


# -----------------------------
# Node 2: Calculate Discriminant
# -----------------------------
def calculate_discriminant(state: QuadState):
    d = (state["b"] ** 2) - (4 * state["a"] * state["c"])
    return {"discriminant": d}


# -----------------------------
# Node 3: Find Nature of Roots
# -----------------------------
def find_roots(state: QuadState):
    d = state["discriminant"]

    if d > 0:
        result = "Two distinct real roots"
    elif d == 0:
        result = "One real root"
    else:
        result = "Complex roots"

    return {"result": result}


# -----------------------------
# Build Graph
# -----------------------------
graph = StateGraph(QuadState)

# Add nodes
graph.add_node("show_equation", show_equation)
graph.add_node("calculate_discriminant", calculate_discriminant)
graph.add_node("find_roots", find_roots)

# Flow
graph.set_entry_point("show_equation")

graph.add_edge("show_equation", "calculate_discriminant")
graph.add_edge("calculate_discriminant", "find_roots")
graph.add_edge("find_roots", END)

# Compile graph
app = graph.compile()


# -----------------------------
# Run Example
# -----------------------------
if __name__ == "__main__":
    input_data = {
        "a": 1,
        "b": -3,
        "c": 2
    }

    result = app.invoke(input_data)

    print("\n--- OUTPUT ---")
    print("Equation:", result["equation"])
    print("Discriminant:", result["discriminant"])
    print("Result:", result["result"])