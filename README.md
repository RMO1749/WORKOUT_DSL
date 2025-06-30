# WorkoutDSL

**WorkoutDSL** is a domain-specific language designed to help users define and manage custom fitness routines using a simple, human-readable syntax.

## 🏋️‍♂️ Domain

Fitness and workout planning — for trainers, enthusiasts, or fitness apps.

## 🎯 Purpose

This DSL enables users to:

- Create workouts by name
- Set goals
- Add exercises with sets/reps or durations
- Insert rest periods
- Schedule routines on specific days

## 📄 Example DSL Script

```
create workout "Full Body"
set goal "General Fitness"

add exercise "pushups" for 3 sets of 15
rest 30 seconds
add exercise "plank" for 60 seconds
add exercise "squats" for 4 sets of 12

repeat Monday, Wednesday, Friday
save workout
```

## 🛠️ How It Works

1. DSL scripts are parsed using a Python interpreter.
2. Valid commands are converted to structured workout plans (in JSON).
3. Errors in syntax are caught and reported to the user.

## 🚀 Running the Interpreter

The interpreter can be executed using Python:

```bash
# Clone the repository
git clone https://github.com/your-username/WorkoutDSL.git

# Navigate into the project directory
cd WorkoutDSL

# Run the interpreter on an example DSL script
python interpreter.py examples/full_body.dsl

```
## 📁 Folder Structure
WorkoutDSL_Project/
│
├── examples/
│   ├── full_body.dsl
│   ├── hiit.dsl
│   └── core_crusher.dsl
│
└── interpreter.py       # Your main interpreter script
```

## 🔍 Testing & Debugging

- Includes line-by-line error reporting for invalid DSL syntax.
- Ensures exercises, rest commands, and schedule are correct
Designed for simplicity, flexibility, and easy integration with fitness tools or apps.
