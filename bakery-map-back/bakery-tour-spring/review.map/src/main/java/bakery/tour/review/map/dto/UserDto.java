package bakery.tour.review.map.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class UserDto {

    private Long id;

    @NotBlank @Email
    private String email;

    private String password;
    private String nickname;
    private String image;
    private Integer point;
    private String level_name;
}
