package bakery.tour.review.map.repository;

import bakery.tour.review.map.domain.User;
import lombok.NonNull;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    Optional<User> findByNickname(String nickname);

//    @Query("SELECT u FROM User u WHERE u.age >= :age")
//    List<User> findByAgeGreaterThanEqual(@Param("age") Integer age);
}
