#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <memory>
#include <unordered_set>

#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/filter/zstd.hpp>

#include "chess.hpp"
#include "parse.hpp"

using namespace Comber;

int main(int argc, char** argv) {
    if (argc != 2)
    {
        std::cerr << "Invalid number of arguments" << std::endl;
        return EXIT_FAILURE;
    }

    std::unordered_set<std::string> blocklist = parse_list("blocklist");
    std::unordered_set<std::string> whitelist = parse_list("whitelist");

    std::cout << "Parsed " << blocklist.size() << " names from blocklist" << std::endl;
    std::cout << "Parsed " << whitelist.size() << " names from whitelist" << std::endl;

    std::filesystem::path pgn_path(argv[1]);
    std::ifstream         pgn_file(pgn_path, std::ifstream::in | std::ifstream::binary);

    if (!pgn_file.is_open())
    {
        std::cerr << "Failed to open file" << std::endl;
        return EXIT_FAILURE;
    }

    boost::iostreams::filtering_istream zstd_in;
    zstd_in.push(boost::iostreams::zstd_decompressor());
    zstd_in.push(pgn_file);

    std::unordered_set<std::string> usernames;

    std::unique_ptr<chess::pgn::Visitor> visitor = std::make_unique<PGNFilter>(
      [&usernames, &whitelist, &blocklist](const std::string& name, int elo) {
          if (usernames.contains(name))
              return;

          if (whitelist.contains(name))
              return;

          if (blocklist.contains(name))
              return;

          usernames.emplace(name);
          std::cout << "Player found: " << name << "  Elo: " << elo << std::endl;
      },
      [](std::size_t count) {
          if (count % 1000000 == 0)
              std::cout << "Processed " << count << " games" << std::endl;
      });

    chess::pgn::StreamParser stream_parser(zstd_in);
    stream_parser.readGames(*visitor);
}
