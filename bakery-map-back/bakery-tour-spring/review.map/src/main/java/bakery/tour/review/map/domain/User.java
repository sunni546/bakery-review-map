package bakery.tour.review.map.domain;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

@Entity
@Table(name = "users")
@Getter @Setter
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id")
    private Long id;

    @NonNull @Email
    @Column(unique = true)
    private String email;

    @NonNull
    private String password;

    @NonNull
    @Column(unique = true)
    private String nickname;

    private String image;
    private int point = 0;

//    @OneToMany(mappedBy = "users")
//    private List<Interest> interests = new ArrayList<>();

//    @OneToMany(mappedBy = "users")
//    private List<Review> reviews = new ArrayList<>();
}
