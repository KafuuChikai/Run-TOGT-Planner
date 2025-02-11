#include "drolib/race/race_track.hpp"
#include "drolib/race/race_params.hpp"
#include "drolib/race/race_planner.hpp"
#include <filesystem>
#include <iostream>

using namespace drolib;

int main(int argc, char** argv) {
  if (argc != 6) {
    std::cerr << "Usage: " << argv[0] << " <config_path> <quad_name> <track_path> <traj_path> <wpt_path>" << std::endl;
    return 1;
  }

  fs::path config_path = argv[1];
  std::string quad_name = argv[2];
  std::string config_name = quad_name + "_setups.yaml";
  std::string track_path = argv[3];
  std::string traj_path = argv[4];
  std::string wpt_path = argv[5];

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
  traj.saveAllWaypoints(wpt_path);

  return 0;
}