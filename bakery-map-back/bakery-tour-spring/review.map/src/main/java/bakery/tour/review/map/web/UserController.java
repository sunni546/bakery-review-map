package bakery.tour.review.map.web;

import bakery.tour.review.map.dto.UserDto;
import bakery.tour.review.map.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequiredArgsConstructor
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    @GetMapping("/me")
    public UserDto readOne(@RequestHeader("Authorization") String authorization) {

        return userService.findByJwt(authorization);
    }

    @PostMapping("/join")
    public void create(@Valid @RequestBody UserDto userDto) {

        userService.join(userDto);
    }

    @PostMapping("/login")
    public Map<String, String> auth(@Valid @RequestBody UserDto userDto) {

        return userService.login(userDto);
    }
}
