#ifndef INTELLIDS_H
#define INTELLIDS_H

#include "glm/glm.hpp"
#include <vector>
#include <list>
#include <stack>
#include <algorithm>

using glm::vec2;
using std::vector;
using std::list;
using std::stack;
using std::find_if;

namespace visualizer
{
  template <class T>
  struct Blob
  {
    public:
      vec2 center;
      float radius; 
      vector<SmartPointer<T>> units;

  }; // Blob


  template <class T>
  list<SmartPointer<Blob<T>>> createBlobs(const list<SmartPointer<T>>& units, const float& defaultRadius)
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
        if(b->units[0]->id == s->id || (find_if(
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


      }
    }

    return blobs;

   
  } // createBlobs()

} // visualizer

#endif // INTELLIDS_H 
