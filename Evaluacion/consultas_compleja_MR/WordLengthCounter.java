import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;

public class WordLengthCount {

    // Mapper que toma como entrada objetos y texto y emite como salida una clave y un valor de longitud de palabra e 1
    public static class TokenizerMapper extends Mapper<Object, Text, IntWritable, IntWritable>{

        private Set<Integer> lengthsToCount = new HashSet<>();

        // Setup (se ejecuta una sola vez antes de la ejecución del maper) el cual se utiliza para leer el archivo de entrada que contiene las longitudes de las palabras a contar.
        public void setup(Context context) throws IOException {
            Configuration conf = context.getConfiguration();
            FileSystem fs = FileSystem.get(conf);
            Path lengthsFilePath = new Path(conf.get("lengthsFile"));
            BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(lengthsFilePath)));
            String line;
            while ((line = reader.readLine()) != null) {
                lengthsToCount.add(Integer.parseInt(line.trim()));
            }
            reader.close();
        }

        // Método map que toma como entrada un objeto clave, un texto y un contexto de mapa y emite una clave y un valor de longitud de palabra e 1 si la longitud de la palabra está en la lista de longitudes a contar
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] words = line.split(" ");
            for (String word : words) {
                int length = word.length();
                if (lengthsToCount.contains(length)) {
                    context.write(new IntWritable(length), new IntWritable(1));
                }
            }
        }
    }

    // Reductor el cual toma como entrada una clave y un conjunto de valores de longitud de palabra y 1 y emite como salida una clave y un valor de longitud de palabra y el número total de palabras con esa longitud.
    public static class IntSumReducer extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
        private IntWritable result = new IntWritable();

        // Método reduce que toma como entrada una clave, un conjunto de valores de longitud de palabra y 1 y un contexto de reducción, y emite una clave y un valor de longitud de palabra y el número total de palabras con esa longitud.
        public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    // Método principal que configura el trabajo Hadoop MapReduce y lo ejecuta
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.set("lengthsFile", "./lengthFile.txt");
        Job job = Job.getInstance(conf, "word length count");
        job.setJarByClass(WordLengthCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

