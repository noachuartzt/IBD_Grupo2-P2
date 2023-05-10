import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;

Configuration conf = new Configuration();
conf.set("wordsFile", "/path/to/words/file");
Job job = Job.getInstance(conf, "word count");


public class WordCount {

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable>{

        private Set<String> wordsToCount = new HashSet<>();

         public void setup(Context context) throws IOException {
            Configuration conf = new Configuration();
            conf.set("wordsFile.txt", "./hadoop-deployment/yarn/jobs/");
            FileSystem fs = FileSystem.get(conf);
            Path wordsFilePath = new Path(conf.get("wordsFile"));
            BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(wordsFilePath)));
            String line;
            while ((line = reader.readLine()) != null) {
                wordsToCount.add(line.trim().toLowerCase());
            }
            reader.close();
        }


        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {
            String line = value.toString();
            String[] words = line.split(",");
            for (String word : words) {
                String cleanedWord = word.trim().toLowerCase();
                if (wordsToCount.contains(cleanedWord)) {
                    context.write(new Text(cleanedWord), new IntWritable(1));
                }
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context
        ) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.setStrings("wordsToCount", args[2].split(","));
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
