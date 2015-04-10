package algorithm;

import java.util.*;
import java.util.Map.Entry;

/**
 * Player:
 * <brief description of class>
 */
public class Player {


    private int playerID;

    private GameSimulator game;

    public Player(int playerID) {
        this.playerID = playerID;
        this.game = new GameSimulator();
    }

    public int makePlay(int[] board) {

        // get all the possible moves
        Queue<Integer> moves = getMoves(playerID, board);
        Map<Integer, double[]> scores = new HashMap<Integer, double[]>();
        Integer move;
        while ((move = moves.poll()) != null) {

            System.out.printf("Move %d\n", move+1);
            System.out.println("=========================================================");
            game.setGameState(board.clone(), playerID);
            game.printBoard();

            int newTurn = simulateMove(move, playerID, board.clone());
            int[] newBoard = game.getBoard().clone();
            scores.put(move, simulateGame(newBoard.clone(), newTurn, "", 8));
            System.out.println("[Enter]");
//            new Scanner(System.in).nextLine();
        }

        // calculate the best move
        int best = calcBestMove(scores);

        return best;
    }

    public double[] simulateGame(int[] board, int turn, String space, int depth) {

        double[] scores = new double[4];

        // Base Case: game over
        if (turn == 0 || board[6] > 18 || board[13] > 18 || depth == 0) {
            if (playerID == 1)
                scores[0] = board[6] - board[13];
            else
                scores[0] = board[13] = board[6];

            if (scores[0] > 0) {
                scores[1] = 1;
//                System.out.println("win");
            } else if (scores[0] == 0) {
                scores[1] = .5;
//                System.out.println("tie");
            } else {
                scores[1] = 0;
//                System.out.println("lose");
            }


            scores[2] = 1;

            if (depth != 0)
                scores[3] = 1;
            else
                scores[3] = 0;

        } else {

            // Get all moves
            Queue<Integer> moves = getMoves(turn,board);

            if (moves.size() > 1)
                space = space.concat("                   ");

            String tmp = "";
            if (!space.isEmpty()) {
                tmp = space;
                space = "";
            }
            // loop through each move
            Integer move;
            while((move = moves.poll()) != null) {
//                System.out.print(space);
                int nextTurn = simulateMove(move, turn, board.clone()); //state.peek().turn, state.peek().board.clone());
                int[] nextBoard = game.getBoard().clone();
                double[] tmpScores = simulateGame(nextBoard.clone(), nextTurn, tmp, depth - 1);
                space = tmp;

                if ((tmpScores[1] == 2) && (tmpScores[2] == 2) && (tmpScores[3] == 1) && turn == playerID) {
                    scores[0] = tmpScores[0];
                    scores[1] = 1;
                    scores[2] = 1;
                    scores[3] = 0;
                    return scores;

                } else {
                    scores[0] += tmpScores[0];
                    scores[1] += tmpScores[1];
                    scores[2] += tmpScores[2];
                    scores[3] = 0;
                }


            }
//            state.pop();
            if (!space.isEmpty())
                space = space.substring(19);


        }

        return scores;
    }

    public Queue<Integer> getMoves(int player, int[] board) {
        Queue<Integer> moves = new LinkedList<Integer>();
        for (int i = 0; i < 6; i++) {
            int pieceIndex = i;
            // adjust if player 2
            if (player == 2)
                pieceIndex += (6 - i) * 2;

            // check if the piece has seeds
            if (board[pieceIndex] > 0)
                moves.add(i); // add the piece to potential moves
        }
        return moves;
    }

    public int simulateMove(int move, int turn, int[] board) {
//        System.out.print("Player:" + turn + " move:" + (move + 1) + " -> ");

        game.setGameState(board.clone(), turn);
//        System.out.println("before");
//        game.printBoard();
        int nextTurn = game.move(move, turn, board.clone());
//        System.out.println("after");
//        game.printBoard();
        return nextTurn;
    }

    public int calcBestMove(Map<Integer, double[]> scores) {
        int bestMove = 0;
        double bestRatio = 0;
        double sum = 0;
        for (Entry<Integer, double[]> curScores : scores.entrySet()) {
            double cur = curScores.getValue()[1] / curScores.getValue()[2];
            System.out.printf("Move:%d Score:%.2f |Sum (diff:%d, wins/lose/tie:%.1f, #games:%d) \n",
                    curScores.getKey()+1, cur, (int) curScores.getValue()[0],
                    curScores.getValue()[1], (int) curScores.getValue()[2]);
            if (cur > bestRatio) {
                bestRatio = cur;
                bestMove = curScores.getKey();
            }
            sum += cur;
        }
        System.out.printf(    "         Sum:%.2f\n", sum);
        return bestMove + 1;
    }

    public void printScores(Map<Integer, Integer[]> scores) {
        for (Integer[] score : scores.values())
            System.out.printf("%d, %d, % d", score[0], score[1], score[2]);
    }


}
