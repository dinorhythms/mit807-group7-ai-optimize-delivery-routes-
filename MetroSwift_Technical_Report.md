
# MetroSwift Technical Report

## Cover Page
**Project Title**
MetroSwift Logistics Ltd. Lagos Route Optimization System

**Course**
MIT807

**Submission Type**
Lecturer Ready Final Version

**Team**
Group 7

## Team Members
| S/N | Name | Matric Number |
|---|---|---|
| 1 | Sofolabo Ebunoluwa Godiya | 249074016 |
| 2 | Adenuga Oluwapelumi Ayomikun | 249074107 |
| 3 | Kazeem Oladehinde Olanrewaju | 249074082 |
| 4 | Adebayo Tosin Esther | 249074192 |
| 5 | Badiru Ismail Kofoworola | 080201050 |
| 6 | Ekundayo Mathew Mayowa | 140408037 |
| 7 | Unuigboje Aisagbonhi Ohimai | 840404062 |
| 8 | Odemakin Victoria Ifeoluwa | 249074010 |
| 9 | Priscilla Oluchukwu Ikeri | 130310014 |
| 10 | Russele Eduje Sharon | 249074275 |

## Abstract
This project presents an AI driven route optimization system for MetroSwift Logistics Ltd. in Lagos. The solution combines predictive travel time modelling with A star search to support efficient route planning, rerouting, and return to base operations from Alausa, Ikeja and other active rider locations.

## Introduction
The system was redeveloped from a generic Lagos route demonstration into a more practical logistics intelligence prototype. It now models delivery operations around a named company case, dynamic rider position, and traffic aware travel time estimation.

## Problem Statement
Delivery riders do not always begin from a fixed depot after each job. A more realistic routing system must support dispatch from the base, rerouting from the field, and return to base decisions while adapting to changing road conditions.

## Objectives
- model a Lagos delivery graph for MetroSwift Logistics Ltd.
- use AI techniques to improve route choice
- support dynamic source selection
- provide lecturer friendly desktop and mobile demonstration versions
- compare A star with BFS and DFS

## Methodology
The solution uses predicted edge costs and A star search as the primary optimization method. BFS and DFS are preserved as baseline graph traversal methods for academic comparison.

## Desktop Version
The desktop application is implemented with Python Tkinter and serves as the main demonstration platform.

## Mobile Version
The mobile version is delivered as a Progressive Web App style prototype with a manifest and service worker for a more polished demonstration experience.

## Testing
The project tests confirm valid route generation for the major search methods and dynamic source routing behavior.

## Conclusion
The final system is more aligned with real delivery logistics in Lagos and is better prepared for academic presentation and lecturer review.
