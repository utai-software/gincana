# Gincana
Gincana is a groundbreaking GIS game that revolutionizes geographic play. Track movements via mobile, enter geofences, earn points, answer location-based questions, and watch videos for an interactive experience. The repository includes both server and Android tracking app, providing everything needed to create and run location-based games. If you understand terms like geospatial data, coordinate systems, remote sensing, and geocoding, you'll enjoy Gincana, UTAI SOFTWARE's solution. It brings together powerful GIS elements like mapping, GPS, geofencing, and spatial analysis to offer real-time, location-aware services. Whether it's buffer zones, vector data, or topology rules, Gincana integrates concepts like waypoints, elevation, and overlay analysis to create a cutting-edge geospatial experience. Perfect for those who live in the world of geospatial intelligence (GEOINT) and location-based services (LBS)!

In this version, the Android app of Gincana Community focuses solely on tracking the location, providing real-time geolocation data to the Django server. This streamlined functionality lays the foundation for more advanced features in future releases while maintaining a focus on core geospatial tracking. The Android app of Gincana Community can be easily modified to fit into various game environments, making it adaptable for interactive geolocation-based games. This flexibility allows developers to customize the app to meet specific gaming needs, integrating geospatial elements like tracking, geofencing, and map-based interactions. An optimal game setup for Gincana Community would involve providing participants with offline (paper) maps, using the Android app solely for checking into geofences. Another exciting variation could divide players into groups of at least two: one player carrying the GPS-enabled device and another stationed at a Control Center, interacting with the systems to guide or strategize. This approach offers a mix of digital tracking and traditional navigation, enhancing the overall experience.

# Gincana, How it works
Gincana is a location-based GIS game that utilizes mobile devices to track players' movements in real-time. Here's how it works:

- Tracking: Players move in the real world while the app tracks their location through GPS.
- Geofences: The game sets virtual boundaries (geofences) in specific areas. When a player enters one, the game triggers events.
- Points System: Players earn points by entering these geofences, completing tasks, or answering questions related to the location.
- Interactive Content: Upon entering a geofence, players may be prompted to answer questions, view videos, or complete challenges, making the game both engaging and educational.
- Multiplayer: Players can compete or collaborate to achieve the highest scores.
- Server Connection: The server manages the game logic, keeps track of scores, and pushes updates to players.

This blend of real-world navigation and digital interaction creates a fun, dynamic geographical game experience.

There are numerous scenarios where this type of gamification could be highly effective. Here are some examples:

- Treasure Hunts and Adventure Races: Participants use printed maps to locate hidden treasures or checkpoints. The Android app would track their progress as they check into each geofence. 
- Outdoor Team-Building Events: Teams could be divided, with one person navigating using a GPS device and the other managing strategy at a control center. This setup encourages communication and coordination.
- Educational Field Trips: Students can explore historical or natural sites with offline maps, while the app tracks their location to ensure they stay within certain zones or check in at important locations.
- Orienteering Competitions: Participants use maps to navigate through terrains, with the app ensuring they hit specific geofenced areas as part of the competition.
- Large-Scale Festivals or Conventions: Attendees could receive paper maps for navigating event zones or stages, using the app to check into locations or earn points for visiting specific areas.
- Emergency Preparedness Drills: Teams simulate disaster scenarios, using maps to navigate the area while the app tracks their movement and ensures they remain within safe zones.
- Military or Tactical Training Simulations: Units use maps for tactical exercises while the app ensures they remain within designated operational areas and log crucial checkpoints.
- City-Wide Exploration Games: Participants explore a city or urban environment using maps, with the app logging their progress as they enter geofenced landmarks or points of interest.
- Environmental Cleanup Campaigns: Volunteers could be divided into teams to clean specific geofenced areas, using the app to track their progress and check in at various clean-up zones.
- Scavenger Hunts for Marketing or Promotions: Brands could use the system to send participants around the city, checking into geofenced retail locations or points of interest for rewards.

These examples show how this hybrid approach of using offline maps and geolocation-based app check-ins can create engaging, interactive experiences across various settings.

In a GIS4Police environment, gamification can be a powerful tool to engage officers and other participants in training, simulation, and operational tasks. Here’s an example of how gamification could be applied:

<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_1.jpeg" alt="Gincana View 1">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_2.jpeg" alt="Gincana View 2">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_3.jpeg" alt="Gincana View 3">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_4.jpeg" alt="Gincana View 4">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_5.jpeg" alt="Gincana View 5">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_6.jpeg" alt="Gincana View 6">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_7.jpeg" alt="Gincana View 7">
<img src="https://raw.githubusercontent.com/utai-software/gincana/refs/heads/main/marketing-collateral/UTAI_SOFTWARE_Gincana_Example_Workflow_8.jpeg" alt="Gincana View 8">


### Inspired on Enemy of the State film (Will Smith)

[Watch the trailer on YouTube](https://www.youtube.com/watch?v=BJjcX--0rvk)

Explanation of the Gincana Based on "Enemy of the State":
Concept: The gincana is a game of strategy, stealth, and quick thinking, set in an environment where players must complete tasks while being monitored by an unseen "state" or authority. The objective is to gather pieces of critical information (data or clues) scattered throughout different locations while avoiding detection by agents of the surveillance system.

Roles:

Players (Targets): Similar to Will Smith’s character in Enemy of the State, the players are ordinary individuals who accidentally come into possession of sensitive information. Their goal is to gather more data from various locations and avoid being caught by the "agents."
Agents (Surveillance): A group of players or moderators takes the role of the "state" or agents, using surveillance tools like cameras, drones (real or simulated), and digital tracking methods to find and stop the targets.
Game Mechanics:

Surveillance Challenge: In certain checkpoints, players will need to complete tasks while being watched by cameras or drones. They must figure out how to avoid detection—whether through hacking devices (puzzles), disabling cameras (finding hidden codes), or navigating around them (stealth).
Data Collection: Critical pieces of information (USB drives, QR codes, or encrypted messages) are hidden in various locations. Players must locate and retrieve these items while being pursued by agents.
Evasion Tactics: Players can use disguises, decoys, and misdirection to escape from the agents. If caught, they might be "interrogated" (given penalties or tasks to complete) before they can resume.
Tech Puzzles: Players might have to solve digital or hacking challenges (decoding messages, bypassing firewalls, or unlocking "data vaults") using smartphones or real-world tools. These puzzles could simulate breaking into a government system or disabling tracking mechanisms.
Objectives: The game could be divided into rounds or levels:

Level 1: Escape Detection: Players start with a map and must reach the first checkpoint without being spotted by surveillance.
Level 2: Data Retrieval: Players find and decode the first clue, leading them to another location, while agents try to track them.
Level 3: Final Mission: The players must upload their collected data to a server or hand it over to a "whistleblower," representing the climax of the game. However, by this stage, the agents are on full alert and have access to better tools to catch them.
Environment: The setting could be a city neighborhood, a school, or a large building complex where surveillance systems like cameras, drones, or agent actors are scattered. Players would feel the same kind of pressure as Will Smith’s character, constantly on the run, unsure who to trust, and needing to outsmart the system.

Technology: To enhance the experience, the game could involve real tech elements like GPS tracking, AR (augmented reality) clues, or phone apps that simulate hacking into secure networks.

Summary:
In this gincana, players would immerse themselves in a world where every move is watched, every decision matters, and their survival depends on their ability to evade detection and gather crucial information. Just like in Enemy of the State, they would feel the tension of being hunted by a faceless and omnipotent system, while using their wits and teamwork to win the game.

