package bakery.tour.review.map.service;

import bakery.tour.review.map.domain.User;
import bakery.tour.review.map.dto.UserDto;
import bakery.tour.review.map.jwt.JwtTokenProvider;
import bakery.tour.review.map.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
    private final JwtTokenProvider jwtTokenProvider;
    private final AuthenticationManagerBuilder authenticationManagerBuilder;

    public UserDto findByJwt(String jwt) {
        long j = jwtTokenProvider.findIdByJwt(jwt);

        User user = userRepository.findById(j).orElseThrow(() -> new NoSuchElementException("User Not Found"));

        UserDto userDto = new UserDto();
        userDto.setId(user.getId());
        userDto.setEmail(user.getEmail());
        userDto.setNickname(user.getNickname());
        userDto.setImage(user.getImage());
        userDto.setPoint(user.getPoint());
        // userDto.setLevelName();

        return userDto;
    }

    @Transactional // 변경
    public void join(UserDto userDto) {

        validateDuplicateUser(userDto);

        User user = new User();
        user.setEmail(userDto.getEmail());
        user.setNickname(userDto.getNickname());

        // 비밀번호 암호화
        String hashedPassword = encoder.encode(userDto.getPassword());
        user.setPassword(hashedPassword);

        userRepository.save(user);
    }

    // 중복 회원 검증
    private void validateDuplicateUser(UserDto userDto) {
        Optional<User> user = userRepository.findByEmail(userDto.getEmail());
        if (user.isPresent()) {
            throw new IllegalStateException("이미 존재하는 이메일입니다. 새로운 이메일을 입력해주세요.");
        }

        user = userRepository.findByNickname(userDto.getNickname());
        if (user.isPresent()) {
            throw new IllegalStateException("이미 존재하는 닉네임입니다. 새로운 닉네임을 입력해주세요.");
        }
    }

    @Transactional
    public Map<String, String> login(UserDto userDto) {

        String email = userDto.getEmail();
        String password = userDto.getPassword();

        // 1. MemberEmail, Password로 Member 조회
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalStateException("1로그인에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요."));
        if (!encoder.matches(password, user.getPassword())) {
            throw new IllegalStateException("2로그인에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.");
        }

        // 2. 토큰 생성
        Map<String, String> map = new HashMap<>();

        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(email, password);
        // authenticate 매서드가 실행될 때 CustomUserDetailsService 에서 만든 loadUserByUsername 메서드가 실행
        Authentication authentication = authenticationManagerBuilder.getObject().authenticate(authenticationToken);

        map.put("jwt", jwtTokenProvider.makeJwtToken(user.getId(), authentication));

        return map;
    }
}
