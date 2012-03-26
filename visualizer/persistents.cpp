#include "persistents.h"

namespace visualizer
{


  ostream& operator <<( ostream& os, const glm::vec2& v )
  {
    os << "(" << v.x << ", " << v.y << ")";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::vec4& v )
  {
    os << "(" << v.x << ", " << v.y << ", " << v.z << ", " << v.w << ")";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::mat4x2& m )
  {

    os << "[" << m[0] << ", " << endl;
    os << m[1] << endl;
    os << m[2] << endl;
    os << m[3] << "]";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::mat4& m )
  {
    os << "[" << m[0] << ", " << endl;
    os << m[1] << endl;
    os << m[2] << endl;
    os << m[3] << "]";
    return os;
  }



} // visualizer
