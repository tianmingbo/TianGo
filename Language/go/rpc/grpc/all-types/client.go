package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/durationpb"
	"google.golang.org/protobuf/types/known/emptypb"
	"google.golang.org/protobuf/types/known/structpb"
	"google.golang.org/protobuf/types/known/timestamppb"
	"google.golang.org/protobuf/types/known/wrapperspb"

	"lGo/rpc/grpc/all-types/pb"
)

func main() {
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewTypesServiceClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	//所有的数据类型
	req := &pb.AllTypes{
		Scalars: &pb.ScalarTypes{
			Int32Value:    -100,
			Int64Value:    -9223372036854775808, // 最小 int64
			Uint32Value:   4294967295,           // 最大 uint32
			Uint64Value:   18446744073709551615, // 最大 uint64
			Sint32Value:   -2147483648,          // 最小 sint32
			Sint64Value:   9223372036854775807,  // 最大 sint64
			Fixed32Value:  4294967295,           // 最大 fixed32
			Fixed64Value:  18446744073709551615, // 最大 fixed64
			Sfixed32Value: -2147483648,          // 最小 sfixed32
			Sfixed64Value: 9223372036854775807,  // 最大 sfixed64
			FloatValue:    3.1415926,
			DoubleValue:   3.14159265358979323846,
			BoolValue:     true,
			StringValue:   "Hello, gRPC!",
			BytesValue:    []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}, // "Hello"
		},
		Complex: &pb.ComplexTypes{
			Color: pb.Color_RED,
			InnerMessage: &pb.InnerMessage{
				Name: "InnerMessage",
			},
			MapMessage: map[int32]*pb.InnerMessage{
				1: {Name: "InnerMessage1"},
				2: {Name: "InnerMessage2"},
			},
			Names:   []string{"Name1", "Name2"},
			Numbers: []int32{1, 2, 3},
			MapValue: map[string]int32{
				"Key1": 1,
				"Key2": 2,
			},
		},
		Special: &pb.SpecialTypes{
			Timestamp: &timestamppb.Timestamp{
				Seconds: 10,
			},
			Duration: &durationpb.Duration{
				Seconds: 10,
			},
			Empty: &emptypb.Empty{},
			Dynamic: &structpb.Struct{
				Fields: map[string]*structpb.Value{
					"name":   structpb.NewStringValue("tian"),
					"age":    structpb.NewNumberValue(18),
					"sex":    structpb.NewBoolValue(true),
					"height": structpb.NewNumberValue(1.8),
					"hobby": structpb.NewListValue(&structpb.ListValue{
						Values: []*structpb.Value{
							structpb.NewStringValue("reading"),
							structpb.NewStringValue("coding"),
						},
					}),
				},
			},
		},
		Wrappers: &pb.WrapperTypes{
			Int32Value:  wrapperspb.Int32(1),
			Int64Value:  wrapperspb.Int64(-2),
			Uint32Value: wrapperspb.UInt32(4294967295),
			Uint64Value: wrapperspb.UInt64(18446744073709551615),
			FloatValue:  wrapperspb.Float(5.0),
			DoubleValue: wrapperspb.Double(3.1415926),
			BoolValue:   wrapperspb.Bool(true),
			StringValue: wrapperspb.String("hello"),
			BytesValue:  wrapperspb.Bytes([]byte("world")),
		},
	}
	res, err := c.TestAllTypes(ctx, req)
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	fmt.Println("Response from server:", res)
}
