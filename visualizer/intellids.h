#ifndef INTELLIDS_H
#define INTELLIDS_H

#include "glm/glm.hpp"
#include <vector>
#include <list>
#include <stack>
#include <algorithm>

using glm::vec2;
using glm::sin;
using glm::orientedAngle;
using glm::normalize;
using glm::rotate;
using std::vector;
using std::list;
using std::stack;
using std::find_if;
using std::sort;
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


  template <class T>
  list<SmartPointer<Blob<T>>> createBlobs(const list<SmartPointer<T>>& units, const float& defaultRadius, const float& buffer)
  {

    // replace with faster data structure for searching
    list<int> usedUnits;
    stack<SmartPointer<Blob<T>>> possiblobs;
    list<SmartPointer<Blob<T>>> blobs;

    for(auto& i: units)
    {
      SmartPointer<Blob<T>> t = new Blob<T>;
      t->units.push_back(i);
      t->radius = defaultRadius;
      t->center = i->position;
      possiblobs.push(t);
    }

    while(possiblobs.size())
    {
      auto b = possiblobs.top();
      possiblobs.pop();

      bool shipAdded = false;

      for(auto& s: units)
      {
        // is the id in the usedUnits. 
        if(b->units[0]->id != s->id  // We don't want to test against our own unit
            && (find_if(
              usedUnits.begin(), 
              usedUnits.end(), 
              [&](const int& c) { return c == s->id; }) == usedUnits.end()))
        {
          if(glm::distance(b->center, s->position) < b->radius)
          {
            shipAdded = true;
            b->units.push_back(s);
            usedUnits.push_back(s->id);
            // Within radius.
          }
        }
      }

      if(shipAdded)
      {
        possiblobs.push(b);

        if(find_if(blobs.begin(), blobs.end(), [&](const SmartPointer<Blob<T>>& blob) { return blob == b; }) == blobs.end())
        {
          blobs.push_back(b);
        }

        b->center = vec2(0, 0);
        for(auto& i: b->units)
        {
          b->center += i->position;
        }
        b->center /= b->units.size();


        float distToCenter = 0;
        for(auto& i: b->units)
        {
          distToCenter += glm::distance(i->position, b->center);
        }
        distToCenter /= b->units.size();

        b->radius = distToCenter + defaultRadius;
      }
    }

    for(auto& b: blobs)
    {
      sort(
          b->units.begin(), 
          b->units.end(), 
          [&b] (const SmartPointer<T>& lhs, const SmartPointer<T>& rhs) 
          {
            return glm::distance(lhs->position, b->center) > glm::distance(rhs->position, b->center); 
          });

      // The units should now be sorted by distance from center.

      list<float> availableAngles;
      
      // we want to divide by size+1 because 0 and 360 are the same
      float interval = 2 * 3.14159265358 / (b->units.size() + 1);
      for(size_t i = 0; i < b->units.size(); i++)
      {
        availableAngles.push_back(i * interval);
      }

      for(size_t i = 0; i < b->units.size(); i++)
      {
        auto &u = b->units[i];

        float bestAngle = *min_element(
            availableAngles.begin(),
            availableAngles.end(), 
            [&u, &b] (const float& lhs, const float& rhs) { 
              float angle = orientedAngle(vec2(1, 0), normalize(u->position - b->center));
              return (angle - lhs < angle - rhs);
            });

        availableAngles.remove(bestAngle);

        vec2 id = rotate(vec2(1, 0) * (b->radius + buffer * sin(bestAngle)), bestAngle);
        id += b->center;

        b->idPositions.push_back(id);
        
      }
      
    }

    for(auto& i: units)
    {
      if(find_if(
              usedUnits.begin(), 
              usedUnits.end(), 
              [&i](const int& c) { return c == i->id; }) == usedUnits.end())
      {
        SmartPointer<Blob<T>> t = new Blob<T>;
        t->units.push_back(i);
        t->idPositions.push_back(i->position);
        blobs.push_back(t);
      }
    }

    return blobs;
   
  } // createBlobs()

} // visualizer

#endif // INTELLIDS_H 
