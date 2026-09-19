#include "gtest/gtest.h"
#include "Types.h"
#include "Player.h"
#include "PlatformManager.h"

namespace
{
int randFuncIndex = 0;
float mockRandomFuncFromArray(float min = 0.0f, float max = 0.0f) 
{
    const std::vector<float>randomValues = {10.0f, 20.0f, 30.0f, 40.0f, 50.0f};
    return randomValues[(randFuncIndex++) % randomValues.size()];
}
}

TEST(PlayerTest, JumpVelocityShouldBeSetCorrectly)
{
    const ScreenSize screenSize{500, 700};
    Player::Config config;
    config.jumpVelocityY = 913.0f;
    Player player(screenSize, config);
    player.jump();

    ASSERT_EQ(player.velocityY(), config.jumpVelocityY);
}

TEST(PlayerTest, PlayedShouldFallUnderTheGravity) 
{
    const ScreenSize screenSize{500, 700};
    Player::Config config;
    Player player(screenSize, config);

    player.update(1.0f);

    const float initialY = screenSize.height * 0.5f - config.initialOffsetY;
    ASSERT_EQ(player.y(), initialY + config.gravity);
}

TEST(PlatformManagerTest, PlatformPositionsShouldSetCorrectly) 
{
    const ScreenSize screenSize{500, 700};
    PlatformManager platformManager(screenSize, mockRandomFuncFromArray);

    const float platformCount = 10;
    const auto platforms = platformManager.platforms();
    ASSERT_EQ(platforms.size(), platformCount);

    randFuncIndex = 0;
    const float verticalSpacing = static_cast<float>(screenSize.height) / platformCount;
    for (int i = 0; i < platforms.size(); ++i)
    {
        const float expectedX = mockRandomFuncFromArray();
        const float expectedY = i * verticalSpacing + mockRandomFuncFromArray();

        EXPECT_NEAR(platforms[i].x, expectedX, 0.001f);
        EXPECT_NEAR(platforms[i].y, expectedX, 0.001f);
    }
}

int main(int argc, char** argv)
{
    testing::InitGoogleTest(&argc, argv);
    const auto status = RUN_ALL_TESTS(); 
    std::cin.get();
    return status;
}