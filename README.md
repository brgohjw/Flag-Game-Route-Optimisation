# Flag-Game-Route-Optimisation
Minimising distance travelled by players in a flag collection game using a randomised 2-opt heuristic

## Task 1: Single Player (single_player.py)
You are a player in this game. The objective is to collect at least p points. (Since players run at the same speed, this means that you want to minimize the distance taken in your route.) It does not matter how many points you manage to accumulate; as long as you get at least p points. Plan the route that you will take in your attempt to win the game. There are two variations of this game:
(i) In the first variation, players stop at the last flag in their route to end the game; there
is no need to move back to the SP.
(ii) in the second variation, all players must get back to the SP to end the game.

In both variations, the objective is still the same: minimize the distance the player has to travel to collect at least p points.

## Task 2: n-Players (n_players.py)
You manage a team of n players in this game (where n is a number from 1 to 8). The rules and objective of the game is the same as for Q1 except that: 
(i) Players in your team do not get points for touching the same flag more than once. If player 1 has already touched F0009, no other player in your team should touch the same flag. 
(ii) The total number of points collected by the whole team need to be at least p to end the game.

Plan the routes for each player in your team so as to minimize the total distance travelled by all players in order to collect at least p points as a team.

## Randomised 2-Opt Optimisation Algorithm 
Randomised variant was used to increase efficiency, as compared to brute force 2 opt

1. Iterate len(route) * 10 times. In each iteration:
  a. Generate a random i index, and generate a random j index
  b. Swap 2 nodes based on these indices, where new_route[i:j+1] = new_route[j:i-1:-1]
  c. If distance of new_route is lower than distance of current best route, update best route and best route distance
2. Return best route
