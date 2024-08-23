package bakery.tour.review.map.repository;

import bakery.tour.review.map.domain.User;
import lombok.NonNull;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @NonNull Optional<User> findById(@NonNull Long id);

    Optional<User> findByEmail(String email);

    Optional<User> findByNickname(String nickname);
}
