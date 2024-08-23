package bakery.tour.review.map.domain;

import lombok.Getter;

@Getter
public enum Level {
    STARTER("초심자", 0),
    BEGINNER("하수", 100),
    INTERMEDIATE("중수", 1000),
    EXPERT("고수", 10000);

    private final String name;
    private final int point;

    private Level(String name, int point) {
        this.name = name;
        this.point = point;
    }

    public static Level getLevelByPoint(int point) {

        if (point < 0) {
            throw new IllegalArgumentException("point must be greater than or equal to 0");
        }

        Level level = null; // not found

        for (Level newLevel : Level.values()) {
            if (newLevel.point > point) {
                break;
            }

            level = newLevel;
        }
        return level;
    }
}
