#include "crow_all.h"

int main()
{
  crow::SimpleApp app;

  CROW_ROUTE(app, "/")
  ([](){
      return "Hello world";
  });

  crow::logger::setLogLevel(crow::LogLevel::CRITICAL);

  app.port(8081)
      // .multithreaded()
      .run();
}
