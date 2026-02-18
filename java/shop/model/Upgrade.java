package shop.model; 
// !!THIS FILE IS DONE. DO NOT CODE ANYMORE HERE. 
// shop/model/ is where we will put the data and rules, not stuff w/ screens/clicks 
// shop/model/Upgrade.java is where the idea of the upgrades will be eg. cost, effect, name, description, etc. 
public class Upgrade {

    // data for the upgrades 
    private String name;
    private int cost;
    private String description;

    private String statAffected;      // "speed", "power", etc.
    private double bonusAmount;       // 1 or 1.05
    private boolean percentageBased;  // false = +1, true = ×1.05
    private boolean oneTimeUse;
    private boolean permanent;
    

    public Upgrade(
            String name,
            int cost,
            String description,
            String statAffected,
            double bonusAmount,
            boolean percentageBased,
            boolean oneTimeUse,
            boolean permanent
    ) {
        this.name = name;
        this.cost = cost;
        this.description = description;
        this.statAffected = statAffected;
        this.bonusAmount = bonusAmount;
        this.percentageBased = percentageBased;
        this.oneTimeUse = oneTimeUse;
        this.permanent = permanent;
    }

    // getters only
    public String getName() {
        return name;
    }

    public int getCost() {
        return cost;
    }

    public String getDescription() {
        return description;
    }

    public String getStatAffected() {
        return statAffected;
    }

    public double getBonusAmount() {
        return bonusAmount;
    }

    public boolean isPercentageBased() {
        return percentageBased;
    }

    public boolean isOneTimeUse() {
        return oneTimeUse;
    }

    public boolean isPermanent() {
        return permanent;
    }
    
}
