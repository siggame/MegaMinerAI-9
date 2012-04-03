#ifndef INTELLIDS_H
#define INTELLIDS_H

#include "glm/glm.hpp"
#include <vector>

using glm::vec2;
using std::vector;

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
  void createBlobs()
  {
  } // createBlobs()

} // visualizer

#endif // INTELLIDS_H 
