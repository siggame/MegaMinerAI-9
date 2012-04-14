
import java.util.Vector;

public class Fleet{
	
	public Vector<PseudoShip> fleet;
	public int size;
	
	public Fleet(){
		fleet = new Vector<PseudoShip>();
		size = 0;
	}
	
	public Fleet(Ship[] ships){
		fleet = new Vector<PseudoShip>();
		for(int i = 0; i < ships.length; i++){
			PseudoShip t = new PseudoShip(ships[i]);
			fleet.add(t);
		}
		size = fleet.size();
	}
	
	public Fleet(Ship[] ships, int player){
		fleet = new Vector<PseudoShip>();
		for(int i = 0; i < ships.length; i++){
			if(ships[i].getOwner() == player){
				PseudoShip t = new PseudoShip(ships[i]);
				fleet.add(t);
			}
		}
		size = fleet.size();
	}
	
	public void kill(int index){
		if(index >= size){
			System.out.print("Killing PseudoShip out of range!!");
		}
		fleet.remove(index);
		size--;
	}
	
	public void kill(PseudoShip p){
		for(int i = 0; i < size; i++){
			if(fleet.elementAt(i).id == p.id)
				kill(i);
		}
	}
	
	public PseudoShip at(int index){
		if(index >= size)
			System.out.print("Access PseudoShip out of range!!");
		return fleet.elementAt(index);
	}
	
}













