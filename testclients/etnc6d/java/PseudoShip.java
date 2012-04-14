public class PseudoShip{
	
	public int x,y;
	public int id;
	public String type;
	public int cost;
	public int radius;
	public int range;
	public int damage;
	public int selfDestructDamage;
	public int maxMovement;
	public int maxAttacks;
	public int maxHealth;
	public int owner;
	public int attacksLeft;
	public int movementLeft;
	public int health;
	public Ship self;
	public Fleet ownerFleet;
	
	public PseudoShip(Ship src){
		x = src.getX();
		y = src.getY();
		id = src.getId();
		type = src.getType();
		cost = src.getCost();
		radius = src.getRadius();
		range = src.getRange();
		damage = src.getDamage();
		selfDestructDamage = src.getSelfDestructDamage();
		maxMovement = src.getMaxMovement();
		maxAttacks = src.getMaxAttacks();
		maxHealth = src.getMaxHealth();
		owner = src.getOwner();
		attacksLeft = src.getAttacksLeft();
		movementLeft = src.getMovementLeft();
		health = src.getHealth();
		self = src;
	}
	
	public int move(int x, int y){
		return self.move(x, y);
	}
	
	public int selfDestruct(){
		return self.selfDestruct();
	}
	
	public int attack(PseudoShip target){
		return self.attack(target.self);
	}
	
	
	
}
