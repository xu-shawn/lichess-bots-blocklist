#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <filesystem>
#include <fstream>
#include <string>
#include <string_view>
#include <iomanip>
#include <unordered_set>

#include "chess.hpp"

namespace Comber {

struct PlayerInfo {
    std::string name;
    int         elo;
    bool        is_bot;
};

class PGNFilter: public chess::pgn::Visitor {
   public:
    PGNFilter(std::function<void(const std::string&, int)> name_listener,
              std::function<void(std::size_t)>             count_listener);
    virtual ~PGNFilter() = default;
    virtual void startPgn();
    virtual void header(std::string_view key, std::string_view value);
    virtual void startMoves();
    virtual void move(std::string_view move, std::string_view comment);
    virtual void endPgn();

   private:
    std::function<void(const std::string&, int)> player_listener_;
    std::function<void(int)>                     count_listener_;
    std::array<PlayerInfo, 2>                    players_;
    std::size_t                                  count_;
};

std::unordered_set<std::string> parse_list(std::filesystem::path path);

}  // namespace LichessBot

#endif
