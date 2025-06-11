#include <charconv>
#include <print>
#include <string>
#include <unordered_set>

#include "parse.hpp"
#include "chess.hpp"

namespace Comber {

enum : int {
    WHITE = 0,
    BLACK = 1
};

PGNFilter::PGNFilter(std::function<void(const std::string&, int)> name_listener,
                     std::function<void(std::size_t)>             count_listener) :
    player_listener_{name_listener},
    count_listener_{count_listener},
    players_{},
    count_{} {}

void PGNFilter::startPgn() {
    count_listener_(count_);
    count_++;
    for (auto& player : players_)
    {
        player.name   = "";
        player.elo    = 0;
        player.is_bot = false;
    }
}

void PGNFilter::header(std::string_view key, std::string_view value) {
    if (key == "White")
    {
        players_[WHITE].name = value;
        return;
    }

    if (key == "Black")
    {
        players_[BLACK].name = value;
        return;
    }

    if (key == "WhiteElo")
    {
        std::from_chars(value.begin(), value.end(), players_[WHITE].elo);
        return;
    }

    if (key == "BlackElo")
    {
        std::from_chars(value.begin(), value.end(), players_[BLACK].elo);
        return;
    }

    if (key == "WhiteTitle" && value == "BOT")
    {
        players_[WHITE].is_bot = true;
        return;
    }

    if (key == "BlackTitle" && value == "BOT")
    {
        players_[BLACK].is_bot = true;
        return;
    }
}

void PGNFilter::startMoves() {
    for (const auto& player : players_)
        if (player.is_bot && player.elo >= 2900)
            player_listener_(player.name, player.elo);

    skipPgn(true);
}

void PGNFilter::move(std::string_view move, std::string_view comment) {}

void PGNFilter::endPgn() {}

std::unordered_set<std::string> parse_list(std::filesystem::path path) {
    std::ifstream                   file(path);
    std::unordered_set<std::string> list{};

    if (!file.is_open())
    {
        std::cerr << "Failed to open file " << path << std::endl;
        return list;
    }

    std::string line;

    while (std::getline(file, line))
        list.insert(std::move(line));

    return list;
}

}
