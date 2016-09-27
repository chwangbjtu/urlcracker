#ifndef __PROTO_REGISTER_H
#define __PROTO_REGISTER_H


class proto_register
{
public:
	proto_register(){};
	~proto_register(){};
	int start();
private:
	static bool init;
};
#endif //__PROTO_REGISTER_H



