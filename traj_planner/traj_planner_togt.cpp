#include "drolib/race/race_track.hpp"
#include "drolib/race/race_params.hpp"
#include "drolib/race/race_planner.hpp"
#include <filesystem>
#include <iostream>

using namespace drolib;

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "Usage: " << argv[0] << " <quad_name> <track_name> <traj_name> <wpt_name>" << std::endl;
    return 1;
  }

  std::string quad_name = argv[1];
  std::string config_name = quad_name + "_setups.yaml";
  std::string track_name = argv[2];
  std::string traj_name = argv[3];
  std::string wpt_name = argv[4];

  fs::path cwd = std::filesystem::current_path();
  fs::path config_path = cwd / ".." / "parameters" / quad_name;
  fs::path track_path = cwd / ".." / "resources/racetrack" / track_name;
  fs::path traj_path = cwd / ".." / "resources/planner/traj" / traj_name;
  fs::path wpt_path = cwd / ".." / "resources/planner/wpt" / wpt_name;

  auto raceparams = std::make_shared<RaceParams>(config_path, config_name);
  auto raceplanner = std::make_shared<RacePlanner>(*raceparams);
  auto racetrack = std::make_shared<RaceTrack>(track_path);

  if (!raceplanner->planTOGT(racetrack)) {
    std::cerr << "Failed to plan trajectory." << std::endl;
    return 1;
  }

  TrajExtremum extremum = raceplanner->getExtremum();
  std::cout << extremum << std::endl;

  MincoSnapTrajectory traj = raceplanner->getTrajectory();
  traj.save(traj_path);  
  traj.saveSegments(wpt_path, 1);

  return 0;
}