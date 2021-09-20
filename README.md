# Tic Tac Toe Engine

This program is an unbeatable Tic Tac Toe engine that in it's worst case ties
the player. The algorithm follows the rules used by Newell and Simon's 1972
tic-tac-toe program.

### The Rules
1. Win: If the player has two in a row, they can place a third to get three in
a row.
2. Block: If the opponent has two in a row, the player must play the third
themselves to block the opponent.
3. Fork: Cause a scenario where the player has two ways to win
(two non-blocked lines of 2).
4. Blocking an opponent's fork: If there is only one possible fork for the
opponent, the player should block it. Otherwise, the player should block all
forks in any way that simultaneously allows them to make two in a row.
Otherwise, the player should make a two in a row to force the opponent into
defending, as long as it does not result in them producing a fork. For example,
if "X" has two opposite corners and "O" has the center, "O" must not play a
corner move to win. (Playing a corner move in this scenario produces a fork
for "X" to win.)
5. Center: A player marks the center. (If it is the first move of the game,
playing a corner move gives the second player more opportunities to make a
mistake and may therefore be the better choice; however, it makes no
difference between perfect players.)
6. Opposite corner: If the opponent is in the corner, the player plays the
opposite corner.
7. Empty corner: The player plays in a corner square.
8. Empty side: The player plays in a middle square on any of the four sides.