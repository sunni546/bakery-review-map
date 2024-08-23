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
    private Integer point = 0;

    @Enumerated(EnumType.STRING)
    private Level level = Level.STARTER;

//    @ManyToOne(fetch = FetchType.LAZY)
//    @JoinColumn(name = "level_id")
//    private Level level;

//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
//    private List<Interest> interests = new ArrayList<>();
//
//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
//    private List<Review> reviews = new ArrayList<>();
}
