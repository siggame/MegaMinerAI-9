#ifndef INTELLIDS_H
#define INTELLIDS_H

#include "glm/glm.hpp"
#include "glm/gtx/random.hpp"
#include <vector>
#include <list>
#include <stack>
#include <map>
#include <algorithm>

using glm::vec2;
using glm::sin;
using glm::orientedAngle;
using glm::normalize;
using glm::distance;
using glm::rotate;
using std::vector;
using std::list;
using std::stack;
using std::find_if;
using std::sort;
using std::map;
using std::min_element;

namespace visualizer
{
  template <class T>
  struct Blob
  {
    public:
      vec2 center;
      float radius; 
      vector<SmartPointer<T>> units;
      vector<vec2> idPositions;

  }; // Blob

  struct ID
  {
    public:
      ID() {}
      ID(const vec2& c, const int& i) : center(c), id(i) {}
      vec2 center;
      int id;
  }; // ID


  template <class T>
  list<ID> createIDs(const list<SmartPointer<T>>& units, const float& idRadius, const float& maxMoveDistance)
  {
    list<ID> ids;

    const float angle = 15;

    for(auto& unit: units)
    {
      ID tID;
      tID.id = unit->id;
      bool collision = true;
      for(float radius = unit->radius + idRadius; radius < unit->radius + 500 && collision; radius += 15)
      {
        if(unit->id==11)
        {
          cout << radius << endl;
        }

        for(size_t theta = 0; theta < (360-angle) / angle && collision; theta++)
        {

          tID.center = unit->position + rotate(vec2(0, -1) * radius, theta*angle);

          collision = false;
          for(auto& collider: units)
          {
            if(collision)
              break;

            vec2 u = collider->position;
            if( distance(tID.center, u) < collider->radius + idRadius )
            {
              collision = true;
            }

          }

          for(auto& collider: ids)
          {
            if(collision)
              break;

            if( distance(tID.center, collider.center) < 2 * idRadius )
            {
              collision = true;
            }
          }
          
        }
      }

      ids.push_back(tID);
    }

    return ids;

  } // createIDs()

} // visualizer

#endif // INTELLIDS_H 
