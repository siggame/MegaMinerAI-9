import com.sun.jna.Pointer;
import java.awt.Point;
import java.util.*;
import java.lang.*;

///The class implementing gameplay logic.
public class AI extends BaseAI
{
	// Origin
	// Uno
	// Dos
	// Tres
	// WeaponsPlatform3
	public static String personality = "Tres";
	public static String persona0 = "Dos";
	public static String persona1 = "WeaponsPlatform3";
	public Random gen;
	public static boolean splitPersonality = true;

public String username()
{
	if(splitPersonality)
		if(playerID() == 0)
			return "AI: " + persona0;
		else
			return "AI: " + persona1;
	return ("AI: " + personality);
}
public String password()
{
	return "12345";
}

//This function is called each time it is your turn
//Return true to end your turn, return false to ask the server for updated information
public boolean run()
{
	if(splitPersonality){
		if(playerID() == 0){
			decisionEngine(persona0);
		}else{
			decisionEngine(persona1);
		}
	}else{
		decisionEngine(personality);
	}
	
	return true;
}

public void decisionEngine(String persona){
	if(persona.equals("Origin"))
		aiOrigin();
	else if(persona.equals("Uno"))
		aiUno();
	else if(persona.equals("Dos"))
		aiDos();
	else if(persona.equals("Tres"))
		aiTres();
	else if(persona.equals("WeaponsPlatform3"))
		aiWeaponsPlatform3();
	else
		System.out.print("Unknown Personality");
}

//This function is called once, before your first turn
public void init() {
	gen = new Random();
	
}

//This function is called once, after your last turn
public void end() {}

public AI(Pointer c)
{
	super(c);
}
  
public void aiOrigin(){
	System.out.println("Starting turn " + turnNumber() + " of round " + roundNumber());
	// Find each player's warp gate
	int myGateIndex=0, theirGateIndex=0;
	for(int i = 0; i < ships.length; i++)
	{
		// If this ship is of type Warp Gate
		if(ships[i].getType().compareTo("Warp Gate") == 0)
		{
			// If you own this ship
			if(ships[i].getOwner() == playerID())
			{
				myGateIndex = i;
			}
				else
			{
				theirGateIndex = i;
			}
		}
	}

	// Warp in some ships
	for(int i = 0; i < shipTypes.length; i++)
	{
		// If you have enough energy to warp in this type of ship
		if(shipTypes[i].getCost() <= players[playerID()].getEnergy())
		{
			// Warp it in directly on top of your warp gate
			shipTypes[i].warpIn(ships[myGateIndex].getX(), ships[myGateIndex].getY());
		}
	}

	// Command your ships
	for(int i = 0; i < ships.length; i++)
	{
		// if you own this ship, it can move and it can attack
		if(ships[i].getOwner() == playerID() && ships[i].getMovementLeft() > 0 && ships[i].getAttacksLeft() > 0)
		{
			// Find a point on the line connecting this ship and their warp gate that is close enough for this ship to move to.
			// x and y are out parameters
			Point goal = pointOnLine(ships[i].getX(), ships[i].getY(), ships[theirGateIndex].getX(), ships[theirGateIndex].getY(), ships[i].getMovementLeft());
			// If I have to move to get there
			if(ships[i].getX() != goal.x || ships[i].getY() != goal.y)
				ships[i].move(goal.x, goal.y);

			// If the distance from my ship to their warp gate is less than my ships attack range plus their gate's radius
			if(distance(ships[i].getX(), ships[i].getY(), ships[theirGateIndex].getX(), ships[theirGateIndex].getY()) <= ships[i].getRange() + ships[theirGateIndex].getRadius())
			{
				// If their warp gate is still alive
				if(ships[theirGateIndex].getHealth() > 0)
				ships[i].attack(ships[theirGateIndex]);
			}
		}
	}
} // END AI ORIGIN

public void aiUno(){
	System.out.print("Uno: " + new Integer(turnNumber()).toString() + " " + new Integer(roundNumber()).toString() + "\n");
	
	while(players[playerID()].getEnergy() > shipTypes[0].getCost()){
		shipTypes[0].warpIn(ships[playerID()].getX(), ships[playerID()].getY());
	}
	
	for(int i = 0; i < ships.length; i++){
		if(ships[i].getOwner() == playerID()){
			ships[i].move(ships[i].getX() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)), 
				ships[i].getY() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)));
		}
	}
	
	for(int i = 0; i < ships.length; i++){
		for(int j = 0; j < ships.length; j++){
			if(ships[i].getOwner() == this.playerID()){
				if(ships[j].getOwner() != playerID()){
					ships[i].attack(ships[j]);
				}
			}
		}
	}
}

public void aiDos(){
	System.out.print("Dos: " + new Integer(turnNumber()).toString() + " " + new Integer(roundNumber()).toString() + "\n");
	
	while(players[playerID()].getEnergy() >= shipTypes[0].getCost()){
		shipTypes[0].warpIn(ships[playerID()].getX(), ships[playerID()].getY());
	}
	
	for(int i = 0; i < ships.length; i++){
		if(ships[i].getOwner() == playerID()){
			if(gen.nextFloat() < .3){
				int k = playerID() == 0 ? 1 : 0;
				Point loc = pointOnLine(ships[i].getX(), ships[i].getY(), ships[k].getX(),
					ships[k].getY(), ships[i].getMaxMovement());
				ships[i].move(loc.x, loc.y);
			}else{
				ships[i].move(
					ships[i].getX() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)), 
					ships[i].getY() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)));
			}
		}
	}
	
	for(int i = 0; i < ships.length; i++){
		for(int j = 0; j < ships.length; j++){
			if(ships[i].getOwner() == this.playerID()){
				if(ships[j].getOwner() != playerID() && 
						distance(ships[i].getX(), ships[i].getY(), ships[j].getX(), ships[j].getY()) < ships[i].getRange()){
					ships[i].attack(ships[j]);
				}
			}
		}
	}
}

public void aiTres(){
	System.out.print("Tres: " + new Integer(turnNumber()).toString() + " " + new Integer(roundNumber()).toString() + "\n");
	
	int var = gen.nextInt() % 4;
	while(players[playerID()].getEnergy() >= shipTypes[var].getCost()){
		shipTypes[var].warpIn(ships[playerID()].getX(), ships[playerID()].getY());
		var = gen.nextInt() % 4;
	}
	
	for(int i = 0; i < ships.length; i++){
		if(ships[i].getOwner() == playerID()){
			if(gen.nextFloat() < .3){
				int k = playerID() == 0 ? 1 : 0;
				Point loc = pointOnLine(ships[i].getX(), ships[i].getY(), ships[k].getX(),
					ships[k].getY(), ships[i].getMaxMovement());
				ships[i].move(loc.x, loc.y);
			}else{
				ships[i].move(
					ships[i].getX() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)), 
					ships[i].getY() + (int)(gen.nextFloat() * ships[i].getMaxMovement()/3.0 * (gen.nextBoolean() ? 1 : -1)));
			}
		}
	}
	
	for(int i = 0; i < ships.length; i++){
		for(int j = 0; j < ships.length; j++){
			if(ships[i].getOwner() == this.playerID()){
				if(ships[j].getOwner() != playerID() && 
						distance(ships[i].getX(), ships[i].getY(), ships[j].getX(), ships[j].getY()) < ships[i].getRange()){
					ships[i].attack(ships[j]);
				}
			}
		}
	}
}

public void aiWeaponsPlatform3(){
	System.out.print("WP3: " + new Integer(turnNumber()).toString() + " " + new Integer(roundNumber()).toString() + "\n");
	int wp = -1;
	for(int i = 0; i < 4; i++){
		if(shipTypes[i].getType().equals("Weapons Platform"))
			wp = i;
	}
	if(wp != -1){
		while(players[playerID()].getEnergy() >= shipTypes[wp].getCost()){
			shipTypes[wp].warpIn(ships[playerID()].getX(), ships[playerID()].getY());
		}
		
		for(int i = 0; i < ships.length; i++){
			if(ships[i].getOwner() != playerID() && ships[i].getType().equals("Weapons Platform")){
				int opH = ships[i].getHealth();
				int j = 0;
				while(opH > 0){
					if(ships[j].getOwner() == playerID()){
						ships[j].attack(ships[i]);
						opH -= ships[j].getDamage();
						if(opH <= 0)
							j--;
					}
					j++;
				}
			}
			for(int j = 0; j < ships.length; j++){
				if(ships[j].getOwner() == playerID())
					ships[j].attack(ships[(playerID() == 0) ? 1 : 0]);
			}
		}
	}
	else
		aiDos();
}












} // END AI CLASS
