using System;
using System.IO;
using System.Collections.Generic;

class Program
{
    public static int Main(string[] args)
    {
        BinaryReader reader = new BinaryReader(Console.OpenStandardInput(0)); // read from stdin
        BinaryWriter writer = new BinaryWriter(Console.OpenStandardOutput(0)); // write to stdout
        List<FastByteArray> arrays = new List<FastByteArray>();

        while (true)
        {
            byte action = reader.ReadByte(); // first byte is action
            // Allocate new byte array
            if (action == 1)
            {
                byte length = reader.ReadByte();
                arrays.Add(new FastByteArray(length)); // add FastByteArray of size 0 - 255? (random bytes)
            }
            // Write a section of a byte array to stdout
            else if (action == 2)
            {
                byte index = reader.ReadByte();
                byte offset = reader.ReadByte();
                byte size = reader.ReadByte();
                arrays[index].Write(offset, size, writer);
            }
            // Read into bytearray from stdin
            else if (action == 3)
            {
                byte index = reader.ReadByte();
                byte offset = reader.ReadByte();
                byte size = reader.ReadByte();
                arrays[index].Read(offset, size, reader); // no check of offset or size here means arbitrary mem write
            }
        }
    }
}

class FastByteArray
{
    private byte[] bytes;

    private static Random random = new Random();

    public FastByteArray(int size)
    {
        bytes = new byte[size];
        random.NextBytes(bytes);
    }

    public unsafe void Write(byte index, byte size, BinaryWriter writer)
    {
        fixed (byte* b = bytes)
        {
            for (int i = 0; i < size; i++)
            {
                writer.Write(b[index + i]);
            }
        }
    }

    public unsafe void Read(byte index, byte size, BinaryReader reader)
    {
        fixed (byte* b = bytes)
        {
            for (int i = 0; i < size; i++)
            {
                b[index + i] = reader.ReadByte();
            }
        }
    }
}
