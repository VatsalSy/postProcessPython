/* Title: Getting data from Basilisk file
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
*/
#include "navier-stokes/centered.h"


char filename[80];
int LEVEL;
double xmin, ymin, xmax, ymax;
scalar D2p[];
scalar f[], * interfaces = {f};

event init(t = 0)
{
  restore (file = filename);
  boundary(all);
  N = pow(2,LEVEL);
  foreach() {
    double D11 = (u.x[1,0] - u.x[-1,0]);
    double D22 = (u.y[0,1] - u.y[0,1]);
    double D12 = 0.5*(u.y[1,0] - u.y[-1,0] + u.x[0,1] - u.x[0,1]);
    double D2 = sqrt(sq(D11)+sq(D22)+2.0*sq(D12))/(2*Delta);
    D2p[] = D2/sqrt(2.0);
  }
  boundary ({D2p});

  FILE * fp = ferr;
  output_field ({D2p}, fp, linear = true);
  fclose (fp);
}

int main(int a, char const *arguments[])
{
  sprintf (filename, "%s", arguments[1]);
  LEVEL = atoi(arguments[2]);
  run();
}
