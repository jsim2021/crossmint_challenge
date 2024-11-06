# Crossmint Coding Challenge: Joel's Megaverse

This project is my solution to the Crossmint coding challenge, where I was tasked with creating a **Megaverse** filled with astral objects — 🪐POLYanets, 🌙SOLoons, and ☄comETHs — using the **Megaverse Creator API**.

## Challenge Overview

The challenge includes two main phases and I have split them into separate files:

1. **Phase 1 (phase_one.py)**: Interact with the API to create and validate individual 🪐POLYanets.
2. **Phase 2 (phase_two.py)**: Automate the creation of a larger, uniquely shaped Megaverse.

## Solution Highlights

- **Object-Oriented Design**: I structured the code with classes for different object types, keeping the design clean, modular, and extensible.
- **Error Handling with Exponential Backoff and Jitter**: To handle transient errors when interacting with the API, the solution includes an exponential backoff with jitter for retrying requests, making it resilient to temporary network or server issues.
- **Logging**: Detailed logging has been implemented to track errors of the Megaverse creation process.
- **Abstraction**: Logic is abstracted into classes and methods for readability and reusability, reducing duplication.

## Setup and Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/crossmint-megaverse-solution.git
   cd crossmint-megaverse-solution